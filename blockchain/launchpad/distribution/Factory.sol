// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.20;

import {Owned} from "./lib/solmate/Owned.sol";
import {FixedPointMathLib} from "./lib/solmate/FixedPointMathLib.sol";
import {IUniswapV2Factory} from "./lib/v2-core/interfaces/IUniswapV2Factory.sol";
import {IUniswapV2Pair} from "./lib/v2-core/interfaces/IUniswapV2Pair.sol";
import {GREY} from "./lib/GREY.sol";
import {Token} from "./Token.sol";

contract Factory is Owned {
    using FixedPointMathLib for uint256;

    error MinimumLiquidityTooSmall();
    error TargetGREYRaisedTooLarge();
    error TargetGREYRaisedReached();
    error TargetGREYRaisedNotReached();
    error InsufficientAmountIn();
    error InsufficientAmountOut();
    error InsufficientLiquidity();
    error InsufficientGREYLiquidity();
    error InvalidToken();

    event TokenCreated(address indexed token, address indexed creator);
    event TokenBought(address indexed user, address indexed token, uint256 indexed ethAmount, uint256 tokenAmount);
    event TokenSold(address indexed user, address indexed token, uint256 indexed ethAmount, uint256 tokenAmount);
    event TokenLaunched(address indexed token, address indexed uniswapV2Pair);

    struct Pair {
        uint256 virtualLiquidity;
        uint256 reserveGREY;
        uint256 reserveToken;
    }

    uint256 public constant MINIMUM_VIRTUAL_LIQUIDITY = 0.01 ether;

    GREY public immutable grey;

    IUniswapV2Factory public immutable uniswapV2Factory;

    // Amount of "fake" GREY liquidity each pair starts with
    uint256 public virtualLiquidity;

    // Amount of GREY to be raised for bonding to end
    uint256 public targetGREYRaised;

    // Reserves and additional info for each token
    mapping(address => Pair) public pairs;

    // ======================================== CONSTRUCTOR ========================================

    constructor(address _grey, address _uniswapV2Factory, uint256 _virtualLiquidity, uint256 _targetGREYRaised)
        Owned(msg.sender)
    {
        if (_virtualLiquidity < MINIMUM_VIRTUAL_LIQUIDITY) {
            revert MinimumLiquidityTooSmall();
        }

        grey = GREY(_grey);
        uniswapV2Factory = IUniswapV2Factory(_uniswapV2Factory);

        virtualLiquidity = _virtualLiquidity;
        targetGREYRaised = _targetGREYRaised;
    }

    // ======================================== ADMIN FUNCTIONS ========================================

    function setVirtualLiquidity(uint256 _virtualLiquidity) external onlyOwner {
        if (_virtualLiquidity < MINIMUM_VIRTUAL_LIQUIDITY) {
            revert MinimumLiquidityTooSmall();
        }

        virtualLiquidity = _virtualLiquidity;
    }

    function setTargetGREYRaised(uint256 _targetGREYRaised) external onlyOwner {
        targetGREYRaised = _targetGREYRaised;
    }

    // ======================================== USER FUNCTIONS ========================================

    function createToken(string memory name, string memory symbol, bytes32 salt, uint256 amountIn)
        external
        returns (address tokenAddress, uint256 amountOut)
    {
        Token token = new Token{salt: salt}(name, symbol);
        tokenAddress = address(token);

        pairs[tokenAddress] = Pair({
            virtualLiquidity: virtualLiquidity,
            reserveGREY: virtualLiquidity,
            reserveToken: token.INITIAL_AMOUNT()
        });

        // minAmountOut not needed here as token was just created
        if (amountIn != 0) amountOut = _buyTokens(tokenAddress, amountIn, 0);

        emit TokenCreated(tokenAddress, msg.sender);
    }

    function buyTokens(address token, uint256 amountIn, uint256 minAmountOut) external returns (uint256 amountOut) {
        Pair memory pair = pairs[token];
        if (pair.virtualLiquidity == 0) revert InvalidToken();

        uint256 actualLiquidity = pair.reserveGREY - pair.virtualLiquidity;
        if (actualLiquidity >= targetGREYRaised) {
            revert TargetGREYRaisedReached();
        }

        amountOut = _buyTokens(token, amountIn, minAmountOut);
    }

    function sellTokens(address token, uint256 amountIn, uint256 minAmountOut) external returns (uint256 amountOut) {
        Pair storage pair = pairs[token];
        if (pair.virtualLiquidity == 0) revert InvalidToken();

        uint256 actualLiquidity = pair.reserveGREY - pair.virtualLiquidity;
        if (actualLiquidity >= targetGREYRaised) {
            revert TargetGREYRaisedReached();
        }

        amountOut = _getAmountOut(amountIn, pair.reserveToken, pair.reserveGREY);

        // In theory, this check should never fail
        if (amountOut > actualLiquidity) revert InsufficientGREYLiquidity();

        pair.reserveToken += amountIn;
        pair.reserveGREY -= amountOut;

        if (amountOut < minAmountOut) revert InsufficientAmountOut();

        Token(token).transferFrom(msg.sender, address(this), amountIn);
        grey.transfer(msg.sender, amountOut);

        emit TokenSold(msg.sender, token, amountOut, amountIn);
    }

    function launchToken(address token) external returns (address uniswapV2Pair) {
        Pair memory pair = pairs[token];
        if (pair.virtualLiquidity == 0) revert InvalidToken();

        uint256 actualLiquidity = pair.reserveGREY - pair.virtualLiquidity;
        if (actualLiquidity < targetGREYRaised) {
            revert TargetGREYRaisedNotReached();
        }

        delete pairs[token];

        uint256 greyAmount = actualLiquidity;
        uint256 tokenAmount = pair.reserveToken;

        // Burn tokens equal to ratio of reserveGREY removed to maintain constant price
        uint256 burnAmount = (pair.virtualLiquidity * tokenAmount) / pair.reserveGREY;
        tokenAmount -= burnAmount;
        Token(token).burn(burnAmount);

        uniswapV2Pair = uniswapV2Factory.getPair(address(grey), address(token));
        if (uniswapV2Pair == address(0)) {
            uniswapV2Pair = uniswapV2Factory.createPair(address(grey), address(token));
        }

        grey.transfer(uniswapV2Pair, greyAmount);
        Token(token).transfer(uniswapV2Pair, tokenAmount);

        IUniswapV2Pair(uniswapV2Pair).mint(address(0xdEaD));

        emit TokenLaunched(token, uniswapV2Pair);
    }

    // ======================================== VIEW FUNCTIONS ========================================

    function previewBuyTokens(address token, uint256 amountIn) external view returns (uint256 amountOut) {
        Pair memory pair = pairs[token];
        amountOut = _getAmountOut(amountIn, pair.reserveGREY, pair.reserveToken);
    }

    function previewSellTokens(address token, uint256 amountIn) external view returns (uint256 amountOut) {
        Pair memory pair = pairs[token];

        amountOut = _getAmountOut(amountIn, pair.reserveToken, pair.reserveGREY);

        uint256 actualLiquidity = pair.reserveGREY - pair.virtualLiquidity;
        if (amountOut > actualLiquidity) revert InsufficientGREYLiquidity();
    }

    function tokenPrice(address token) external view returns (uint256 price) {
        Pair memory pair = pairs[token];
        price = pair.reserveGREY.divWadDown(pair.reserveToken);
    }

    function bondingCurveProgress(address token) external view returns (uint256 progress) {
        Pair memory pair = pairs[token];
        uint256 actualLiquidity = pair.reserveGREY - pair.virtualLiquidity;
        progress = actualLiquidity.divWadDown(targetGREYRaised);
    }

    // ======================================== HELPER FUNCTIONS ========================================

    function _buyTokens(address token, uint256 amountIn, uint256 minAmountOut) internal returns (uint256 amountOut) {
        Pair storage pair = pairs[token];

        amountOut = _getAmountOut(amountIn, pair.reserveGREY, pair.reserveToken);

        pair.reserveGREY += amountIn;
        pair.reserveToken -= amountOut;

        if (amountOut < minAmountOut) revert InsufficientAmountOut();

        grey.transferFrom(msg.sender, address(this), amountIn);
        Token(token).transfer(msg.sender, amountOut);

        emit TokenBought(msg.sender, token, amountIn, amountOut);
    }

    function _getAmountOut(uint256 amountIn, uint256 reserveIn, uint256 reserveOut) internal pure returns (uint256) {
        if (amountIn == 0) revert InsufficientAmountIn();
        if (reserveIn == 0 || reserveOut == 0) revert InsufficientLiquidity();

        return (amountIn * reserveOut) / (reserveIn + amountIn);
    }
}

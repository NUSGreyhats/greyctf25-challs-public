// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import {IERC20} from "./lib/IERC20.sol";
import {Rational, RationalLib} from "./lib/Rational.sol";

contract RationalVault {
    IERC20 public asset;

    mapping(address => Rational) internal sharesOf;
    Rational internal totalShares;

    // ======================================== CONSTRUCTOR ========================================

    constructor(address _asset) {
        asset = IERC20(_asset);
    }

    // ======================================== MUTATIVE FUNCTIONS ========================================

    function deposit(uint128 amount) external {
        Rational _shares = convertToShares(amount);

        sharesOf[msg.sender] = sharesOf[msg.sender] + _shares;
        totalShares = totalShares + _shares;

        asset.transferFrom(msg.sender, address(this), amount);
    }

    function mint(uint128 shares) external {
        Rational _shares = RationalLib.fromUint128(shares);
        uint256 amount = convertToAssets(_shares);

        sharesOf[msg.sender] = sharesOf[msg.sender] + _shares;
        totalShares = totalShares + _shares;

        asset.transferFrom(msg.sender, address(this), amount);
    }

    function withdraw(uint128 amount) external {
        Rational _shares = convertToShares(amount);

        sharesOf[msg.sender] = sharesOf[msg.sender] - _shares;
        totalShares = totalShares - _shares;

        asset.transfer(msg.sender, amount);
    }

    function redeem(uint128 shares) external {
        Rational _shares = RationalLib.fromUint128(shares);
        uint256 amount = convertToAssets(_shares);

        sharesOf[msg.sender] = sharesOf[msg.sender] - _shares;
        totalShares = totalShares - _shares;

        asset.transfer(msg.sender, amount);
    }

    // ======================================== VIEW FUNCTIONS ========================================

    function totalAssets() public view returns (uint128) {
        return uint128(asset.balanceOf(address(this)));
    }

    function convertToShares(uint128 assets) public view returns (Rational) {
        if (totalShares == RationalLib.ZERO) return RationalLib.fromUint128(assets);

        Rational _assets = RationalLib.fromUint128(assets);
        Rational _totalAssets = RationalLib.fromUint128(totalAssets());
        Rational _shares = _assets / _totalAssets * totalShares;

        return _shares;
    }

    function convertToAssets(Rational shares) public view returns (uint128) {
        if (totalShares == RationalLib.ZERO) return RationalLib.toUint128(shares);

        Rational _totalAssets = RationalLib.fromUint128(totalAssets());
        Rational _assets = shares / totalShares * _totalAssets;

        return RationalLib.toUint128(_assets);
    }

    function totalSupply() external view returns (uint256) {
        return RationalLib.toUint128(totalShares);
    }

    function balanceOf(address account) external view returns (uint256) {
        return RationalLib.toUint128(sharesOf[account]);
    }
}

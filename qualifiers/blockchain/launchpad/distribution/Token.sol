// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.20;

import {ERC20} from "./lib/solmate/ERC20.sol";

contract Token is ERC20 {
    error NotFactory();

    uint256 public constant INITIAL_AMOUNT = 1000_000e18;

    address public immutable factory;

    constructor(string memory _name, string memory _symbol) ERC20(_name, _symbol, 18) {
        factory = msg.sender;

        _mint(factory, INITIAL_AMOUNT);
    }

    function burn(uint256 amount) external {
        if (msg.sender != factory) revert NotFactory();

        _burn(msg.sender, amount);
    }
}

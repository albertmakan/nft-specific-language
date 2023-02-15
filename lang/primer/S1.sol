// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "./IS1.sol";

contract S1 is IS1 {
    function transfer(address recipient, uint256 amount)
        external
        returns (bool)
    {
        return true;
    }
}

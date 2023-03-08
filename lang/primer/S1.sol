// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "./IS1.sol";
import "@spm/numeric";


function transfer2(address recipient, uint256 amount)
        external
        returns (bool)
{
    S1 s1 = new S1();
    transferToLuka(numeric.add(5, amount));
    return true;
}

function transfer3(address recipient, uint256 amount)
        external
        returns (bool)
{
    transferToLuka(numeric.add(5, amount));
    return true;
}


contract S1 is IS1 {
    event DepositContract(address indexed _from, bytes32 indexed _id, uint104 _value);

    function transfer(address recipient, uint256 amount)
        external
        returns (bool)
    {
        transferToLuka(numeric.add({{fees}}, amount));
        return true;
    }

    function transfer2(address recipient, uint256 amount)
        costs
        returns (bool)
    {
        MILOSPANIC();
        emit DepositContract(recipient, 0, 0);
        transfer3(numeric.add(5, amount));
        return true;
    }

    modifier costs(uint price) {
      if (msg.value >= price) {
         _;
      }
   }
}

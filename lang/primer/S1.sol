// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "./IS1.sol";
import "@spm/numeric";


function transfer2(address recipient, uint256 amount)
        external
        returns (bool)
{
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


contract S1 {
    event DepositContract(address indexed _from, bytes32 indexed _id, Nikola _value);

    struct Nikola {
        address _from;
    }

    function transfer(address recipient, uint256 amount)
        external
        returns (bool)
    {
        transferToLuka(numeric.add({{fees}}, amount));
        return true;
    }

    function transfer2(address recipient, uint256 amount)
        external
        returns (bool)
    {
        emit DepositContract(recipient, 0, Nikola(recipient));
        transfer3(numeric.add(5, amount));
        return true;
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

function add(uint x, uint y) pure returns (uint) {
    return x + y;
}

struct Point {
    uint x;
    uint y;
} 

abstract contract Hello {
    constructor() {

    }

    function hello() pure public returns (string memory) {
        return {{hello}};
    }
}

abstract contract ERC20BASE {

    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value
    );

    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );

    struct ContractData {
        address owner;
        string name;   
    }

    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes calldata) {
        return msg.data;
    }
}
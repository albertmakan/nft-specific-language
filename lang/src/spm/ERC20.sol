// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

struct Nemanja {
    uint8 x;
}


struct Nikola {
    ERC721 x;
    Nemanja n;
}

function approve2(address spender) returns (bool) {
    approve3(spender);
    ERC20.Milos nikola;
    return true;
}

function approve3(address spender) returns (bool) {
    return true;
}

contract ERC20 {
    uint256 public totalSupply;
    mapping(
        address =>uint256
    ) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    string public name = "Solidity by Example";
    string public symbol = "SOLBYEX";
    uint8 public decimals = 18;
    Milos public milos;
    ERC20 public milos20CAO;

    struct Milos {
        uint8 x;
    }

    function transfer(address recipient, uint256 amount)
        external
        returns (bool)
    {
        ERC721 nikolica = new ERC721();
        Milos m = Milos(2);
        balanceOf[msg.sender] -= amount;
        balanceOf[recipient] += amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool) {
        allowance[sender][msg.sender] -= amount;
        balanceOf[sender] -= amount;
        balanceOf[recipient] += amount;
        emit Transfer(sender, recipient, amount);
        return true;
    }
}

contract ERC721 {

    string public symbol = "SOLBYEX";
    uint8 public decimals = 18;

    function mint(uint256 amount) external {
        balanceOf[msg.sender] += amount;
        totalSupply += amount;
        emit Transfer(address(0), msg.sender, amount);
    }

    function burn(uint256 amount) external {
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }
}


contract ERCBASE {

    struct STRUCT_BASE {
        string basee;
    }

    string public VARIABLE_BASE = "NESTO";

    function FUNCTION_BASE() {
        return true;
    }
}

contract ERCINHERIT is ERCBASE {

    struct STRUCT_INHERIT {
        STRUCT_BASE inherited;
    }

    STRUCT_BASE public VARIABLE_INHERIT;

    function FUNCTION_INHERIT() {
        VARIABLE_BASE = VARIABLE_BASE;
        return FUNCTION_BASE();
    }
}
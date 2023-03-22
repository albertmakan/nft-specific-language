// SPDX-License-Identifier: MIT
// NOTE: THIS IMPLEMENTATION IS NOT UP TO ANY SECURITY STANDARDS OR BEST PRACTISES.
// IMPLEMENTATION IS KEPT AS SHORT AS POSSIBLE IN ORDER TO DEMONSTRATE SPM FEATURES

pragma solidity ^0.8.0;

import "./erc20base.sol";

contract ERC20 is ERC20BASE {

    ContractData _data;

    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;
    uint256 private _totalSupply;

    constructor(string memory name_) {
        _data.name = name_;
        _data.owner = _msgSender();
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowances[owner][spender];
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        address owner = _msgSender();
        _transfer(owner, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        address owner = _msgSender();
        _approve(owner, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        address spender = _msgSender();
        _spendAllowance(from, spender, amount);
        _transfer(from, to, amount);
        return true;
    }

    function _transfer(address from, address to, uint256 amount) internal virtual {
        uint256 fromBalance = _balances[from];
        _balances[from] = fromBalance - amount;
        _balances[to] += amount;
        emit Transfer(from, to, amount);
    }

    function _approve(address owner, address spender, uint256 amount) internal virtual {
        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function _spendAllowance(address owner, address spender, uint256 amount) internal virtual {
        uint256 currentAllowance = allowance(owner, spender);
        if (currentAllowance != type(uint256).max) {
            _approve(owner, spender, currentAllowance - amount);
        }
    }

    modifier onlyOwner {
      require(msg.sender == _data.owner);
      _;
   }
}
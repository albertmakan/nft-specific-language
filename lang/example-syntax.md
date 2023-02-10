packages {
  using std.token.numeric.* as numeric
  using custom.equity.sales as sales
  using std.single_owner
  using std.multiple_owners
}

contract Brojko combines {
  numeric.minting
  numeric.balanceChecking
  numeric.burning
  numeric.transfering
}

contract Skemer combines {
  sales with 10% equity and 1% fee
}

contract Tokevestit combines {
  ...
}

administration {
  managed by std.single_owner with $contract_creator owner and ... having partial access {
    to Brojko {
      numeric.minting
      numeric.balanceChecking
      numeric.burning
      numeric.transfering
    }
    to Skemer {
      sales
    }
    to Tokevestit {
      ...
    }
  }
  extended by std.multiple_owners with (<address365>, <address366>, ...) owner having partial access {
    createToken with 3 ownersAgreed
  }
  extended by std.multiple_owners with (<address365>, <address366>, ...) owner having partial access {
    {
      createToken with 3 ownersAgreed
    }
  }
}
plugins {
  using std.token.numeric.* as numeric;
  using custom.equity.sales as sales;
  using std.single_owner;
  using std.multiple_owners;
}

numeric token Brojko supports {
  numeric.minting;
  numeric.balanceChecking;
  numeric.burning;
  numeric.transfering;
}

unique token Skemer supports {
  sales with 10% equity and 1% fee;
}

combined token Tokevestit supports {
  ...
}

administration {
  managed by std.single_owner {
    with owner $contract_creator having partial access {
      to Brojko {
        numeric.minting;
        numeric.balanceChecking;
        numeric.burning;
        numeric.transfering;
      }
      to Skemer {
        sales;
      }
      to Tokevestit {
        ...
      }
    }
  }
  extended by std.multiple_owners {
    with owners (<address365>, <address366>, ...) having partial access {
      createToken with 3 owners agreed;
    }
  }
}
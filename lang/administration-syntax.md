# administrativni deo

- jedan vlasnik
- ima puna prava

- PRIMER 1 single owner
plugins {
  using std.single_owner;
}

administration {
  managed by single_owner {
    with owner $contract_creator having full access;
  }
}

- PRIMER 2 multi-owner
plugins {
  using std.multiple_owners;
}

administration {
  managed by multiple_owners {
    with owners (<address1>, <address2>, ...) having partial access {
      createToken with 5 owners agreed;
      deleteToken with 70% owners agreed;
      destroyContract with all owners agreed;
    }
    with owners (<address365>, <address366>, ...) having partial access {
      createToken with 3 owners agreed;
    }
    .
    .
    .
  }
}

- PRIMER 3 single owner sa slabim permisijama prosiren sa multi-owner
plugins {
  using std.single_owner;
  using std.multiple_owners;
}

administration {
  managed by single_owner {
    with owner $contract_creator having partial access {
      moveFunds;
      deleteContract;
      freezeContract;
    }
  }
  extended by multiple_owners {
    with owners (<address365>, <address366>, ...) having partial access {
      createToken with 3 owners agreed;
    }
  }
}
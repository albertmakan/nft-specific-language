---
sidebar_position: 3
---

# Syntax

An SPL file consists of three main sections: `packages`, `contracts` and `adminitration`.

#### Packages Section

```js
packages {
  using std.package1 [as packageAlias1]
  using std.package2.namespace1 [as packageAlias2]
}
```

You can import another package, based on the namespace. That is done with `using` keyword followed by a dot-separated set of nested namespaces (example `std.contracts.erc20`). You can also define an alias for the imported package, so that it's easier and shorter to reference it when using it.

:::note
When using aliases, you must make sure that they are `unique`.
:::

:::note
All packages must be locally installed using [`spm install`](./cli.md).
:::

#### Contracts Section

```js
contract FirstContract combines {
  packageAlias1.constructor
  packageAlias1.functions.function1 with 1% fee and "Hello" prefix
}
```

You can define one or more constracts that are combining `features` from the previosly imported packages.

A `feature` in the contract can be defined using the following format:

```js
path.to.featureName [with <value1> <param1> [and <value2> <param2> [and ...]]]
```

It includes a fully qualified name of the feature (`FQN`), which is the feature name with dot-separated namespace paths included and template arguments. To make packages more powerful, we support exporting `features` with template arguments from `Solidity` files such as:

```
function function1() {
    uint256 fee = {{ fee: int }};
    string prefix = {{ prefix: str}};
}
```

:::note
The suppurted template argument value types are `Percentage`, `INT`, `FLOAT`, `STRING`, `AddressSet`, `Address`
:::

#### Adminitration Section

```js
packages {
  using package_name.Contract1
  using std.Contract.single_owner
  using std.Contract.multi_owner as multi
}

contract SecondContract combines {
  Contract1.constructor
  Contract1.transfer with 0.1 fee
}

administration {
  managed by single_owner having partial access {
    to SecondContract {
      Contract1.transfer
    }
  }
  extended by multi with [0x1234567890abcdef1234567890ABCDEF12345678] owners having partial access {
    to SecondContract {
      Contract1.transfer
    }
  }
}
```

You can define one managed block and a number of extended blocks. These will result in additional modifiers to functions.
---
sidebar_position: 3
---

# Using packages

SPM packages can be used by other packages, or in Solidity files.

## Using packages in other Packages

SPM language provides a way for you to import an existing package into your own. To do so, just reference them in the import section:

```js
packages {
  using std.package
  using imported.package.contract as contr
}
```

and use them as follows:

```js
package my_own_package {
  nested_package1 {
    @function contr.FunctionName
  }

  nested_package2 {
    @struct std.package.ContractName.StructName
    @struct std.package.GlobalStructName
  }
}

```

## Using packages in Solidity

:::caution
Please note that this feature is still under development and is not available yet!
:::

SPM provides support for using packages in `Solidity` files. To do so, you must import a package as follows:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@spm.std.math";

contract FancyContract {

  function add(uint256 a, uint256 b) public view returns (uint256) {
    return std.math.add(a, b);
  }

  function fancyFibonacci(uint256 a, uint256 b) public view returns (uint256) {
    return std.math.fibonacci(std.math.fibonacci(a), std.math.fibonacci(b));
  }

}
```

In order to successfully compile this `Solidity` file, it first needs to be transpiled to `raw Solidity`. Luckily, SPM CLI provides [a command](./cli.md#transpiling-solidity) for handling this.

:::info
To better understand the relationship between `SPM` and `Solidity`, we can use the analogy of `TypeScript` and `JavaScrip`. Former is a tool that is aiming to improve developer experience, and is just extending the syntax of the latter. For the latter to work, the code first needs to be transpiled to its raw shape - native syntax. For `TypeScript` we use `tsc CLI` to transpile `TS` code to `JS`, while for `SPM` we use `spm CLI` to transpile extended `Solidity` syntax to it's initial form.
:::

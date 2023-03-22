---
sidebar_position: 2
---

# Creating a new package

A new package can be created using `SPM Langugage`.

## SPM Syntax

An SPM package definition file consists of two main sections: `import` and `export`.

#### Import Section

```js
packages {
  using std.package [as packageAlias1]
  using "./local_file.sol" [as packageAlias2]
}
```

You can import another package, based on the namespace. That is done with `using` keyword followed by a dot-separated set of nested namespaces (example `std.contracts.erc20`). You can also define an alias for the imported package, so that it's easier and shorter to reference it when using it.

:::note
When using aliases, you must make sure that they are `unique`.
:::

Another kind of import is from a local file. By saying `using "./local_file.sol"`, you are importing a whole `Solidity` file with all it's definitions, structures and contracts (inheritance and nested file imports are supported).

#### Export Section

In an export section of the package definition, you are able to define what other packages will be able to use. It is a public interface for other packages.

You can define an arbitrary number of nested namespaces, and in those namespaces you can export a certain `feature`.

Just like there are two types of imports, depending on them we can have two types of exports. They do have the same result, but the way you define them is a bit different.

A `feature` is defined in the following format:

```js
[@<type>] path.to.feature [as featureAlias]
```

where a `@type` can be: `@function`, `@struct`, `@contract`, `@event`, or `@modifier`.

:::note
`@type` is optional, if left blank then default value is `@function`.
:::

Feature name is either explicitly defined using an `alias`, or otherwise the default behaviour is to take the last part of the path. So, if the feature path is `path.to.feature.test`, than feature name will be `test`. A fully qualified name of the feature (`FQN`), is the feature name with dot-separated namespace paths included.

:::info
If an export is done from the local `Solidity` file, than `SPM` expects the following format:

`PackageAlias.[ContractName].export_item`.

If `ContractName` is not defined, than `SPM` assumes that `export_item` is somewhere outside of any contract in that `Solidity` file.
:::

```js
package {{package_name}} {
  nested_package1 {
    @function packageAlias1.nested_package.FunctionName
  }

  nested_package2 {
    @struct packageAlias2.ContractName.StructName
    @struct packageAlias2.GlobalStructName
  }
}
```

:::info
Make sure to check our examples on the GitHub!
:::


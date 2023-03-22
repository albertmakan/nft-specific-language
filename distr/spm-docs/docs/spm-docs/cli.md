---
sidebar_position: 5
---

# Using SPM CLI

:::info
It is important to note that all commands except `init` need to be ran from the folder containing `package.json` and `*.spm` files.
:::

## Project Init

The following command will initialize the new project:

```bash
spm init
```

Provide the package name, author and version:

```bash
Package name: my_first_package
Package author: spm-team
Package version (Leave empty for '0.0.1'):
```

:::note
This generates:
- `my_first_package.spm` where you can define the package
- `package.json` with package metadata and dependencies
- _`spm_packages`_ directory where the locally installed packages are stored
:::

The console output of `init` command will include the `private key` that is used for deploying a package.

:::danger
It is important that you keep the generated `private key` safe! Otherwise, you won't be able to publish new versions of that package for the next three months!

Anyone from SPM team would never ask you for your `private key`!
:::

## Package Install

SPM CLI provides a command for installing new packages in your project:

```bash
spm install [<package-name>] [--version <version>]
```

There are two possible scenarios for running the `install` command:
1. You want to add a new package, or update version of the exising one, in your project:
  ```bash
  spm install <package-name> [--version  <version>] 
  ```
  where `<package-name>` is the name of the package that you want to install.
  
  `<version>` can be: 
    - empty (default) which is equivalent to `latest`
    - exact version like `1.0.0` (`<major>.<minor>.<patch>` format)
    

2. You want to install (download) all existing dependencies in your project:
  ```bash
  spm install [--version  <version>] 
  ```
  `<version>` can be: 
    - empty (default) which will pull all versions defined in `package.json`
    - `latest` which will pull latest versions for every package in `package.json`

## Semantic Package Versioning

SPM CLI provides a command for handling semantic package versions:

```bash
spm version [<version>] [--reset]
```
- `<version>` can be:
  - one of the following values: `major`/`minor`/`patch` which will increase that part of version by 1
  - a specific version like `1.0.0` (`<major>.<minor>.<patch>` format) which will set the package version to that specific one
- if `--reset` is provided, that part of version will be set to 0

:::note
If `<version>` is not provided, and `--reset` is passed in, package version will be set to `0.0.0`.
:::

:::caution
While locally, you can use any version you'd like, when trying to deploy a new version to the `SPM Registry` only the versions that are greater than the latest one are allowed.
:::


## Deploying a Package

Before you deploy your package to the `SPM Registry`, you first need to compile it.

SPM CLI provides a command for compiling a package to a single `JSON` file:

```bash
spm pack
```

:::info
This will result in a new file `<package-name>.spm`. This file can be used in other project, or by other packages, and it is what gets deployed to the `SPM Registry`.
:::

Now that your package is compiled, you can deploy it using the following command:

```bash
spm deploy
```

:::caution
This command requires your `private key`.
:::

Done! Your package is ready to be used!

## Transpiling Solidity

:::caution
Please note that this feature is still under development and is not available yet!
:::

```bash
spm transpile <target>
```

where `<target>` can be:
  - path to a specific file: `/path/to/solidity_file.sol`
  - path to a specific folder (project): `/path/to/project/`

:::note
The output of this command is a file or a directory with one or more `.sol` files, that can then be compiled to Ethereum Bytecode using `solc`.
:::
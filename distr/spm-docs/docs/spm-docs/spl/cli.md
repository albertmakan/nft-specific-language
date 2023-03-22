---
sidebar_position: 2
---

# CLI

## Project Init

The following command will initialize the new project:

```bash
spl init <name>
```

:::note
This generates:

- `name.spl` where you can define the packages integration
- `package.json` with dependencies
- _`spm_packages`_ directory where the locally installed packages are stored
:::

:::note
The initialized project will with already installed predefined packages such as std
:::

:::infomation
To install packages, use ```spm install [<package-name>]``` and refer to [spm cli part of documentation](./cli.md)
:::

## Package Combine 

The following command will generate solidity files from each `*.spl` file. The generated output can be used in the same way as every other solidity file (deployed, additionally developed and so on).

```bash
spl combine [<name1>] [<name2> ...]
```

:::note
If the name is not provided as a command argument, then cli will search for all `*.spl` files in the current directory.
:::

---
sidebar_position: 4
---

# Deploying package

In order to deploy a package, take a look at [this guide](./cli.md#deploying-a-package).

# SPM Registry

All packages are stored on `SPM Registry`, which is a distributed database running on top of `IPFS`.

## Rules
In order to have a clean way of managing `SPM packages`, `SPM Registry` defines a certain set of rules that must be followed.

1. Reserving a package name works by the principle: `first one to take`.
2. Each reserved package contains a `public key`, that is valid for maximum `3 months` after the last package update.
3. Owning a package, means owning a corresponding `private key` that is used for signing package versions.
4. Each package version contains a `ECDSA` signature of the following: `<package-name><author><version>`.
5. Owner can `extend ownership` after two months. If he fails to extend it after `3 months` - he loses ownership of the package, than the 1. rule applies.
6. Package versions `can not be changed or modified`, you can only publish new ones. This is to ensure the integrity of the package version, and that it has not been tampered with.


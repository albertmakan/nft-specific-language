---
slug: welcome
title: Welcome
authors: [bjelicaluka, albertmakan, panicmilos, draganaF, nikolapetrovic1]
tags: [solidity, ethereum, smart-contracts, spm, package-management]
---

`SPM` is a tool that aims to improve code reusability in `Solidity` ecosystem, and it is inspired by [NPM](https://npmjs.org).

The main goal is to improve DX (development experience) by introducing the concept of a `package`. A `package` can represent a project solution that can be compiled to a Smart Contract, or it can be a set of utilities that can be used in multiple different projects. The idea is to help Solidity developers by providing them with a tool that can help them find what they need quickly and easily.

<!-- truncate -->

:::info
`SPM` consists of three pieces:

1. [Language](./creating.md) - for creating reusable packages
2. [Registry](./deploying.md) - for distributing packages
3. [CLI](./cli.md) - for using the tool

:::

Another very important thing that `SPM` wants to achieve is ensuring package integrity. In Ethereum, a very important property of Smart Contracts is their `immutability`, i.e. once deployed, they `can not` be updated. That makes Smart Contracts vulnerable to security issues and demands special caution from developers.

This is why, security audits play a very important part in using someone else's code. The aim of `SPM` is to ensure the fact that once a specific package version is deployed, that's it - it `can not` be updated. Hence, a `package` has the same property as Smart Contracts. So that, if the community audits the specific version of a package, and determines that it is `safe to use`, `SPM` will ensure that it does not get modified or changed in any way.

:::note
The hidden benefit of distributing packages and making them publicly available is that more people will get to see them, and find potential security issues. The bigger the community is, the more developers will be able to rely on other packages.
:::

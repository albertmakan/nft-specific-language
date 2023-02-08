# SPM - _Solidity Package Manager_

## Intro

The project consists of three parts:
 - DSL - for defining new packages and integrating existing ones into the project
 - CLI - for running commands and interacting with the tool
 - Package Registry - for storing packages in a remotely accessible network

## Motivation

We've noticed that the syntax for defining a Contract to work with Tokens actually either doesn't take much work, or takes too much work. Namely, either it is necessary to define a _Turing Complete_ language, which there is no point in doing because Solidity already does a good job at that, or it is necessary to define a very simple language that will only specify which standards are used. After additional thinking and discussion, we concluded that it makes the most sense to implement a _Package Manager_ tool for the Solidity ecosystem in general, because such a thing does not exist, but packages must be searched for and installed manually. The DSL that we will implement will serve to define packages, that is, to integrate several different packages, as well as to generate Solidity code based on them. The tool will consist of 3 parts: the previously mentioned DSL (which represents the highest priority for us, offers various benefits to the user such as autocomplete and intellisense, syntax for defining packages, etc.), CLI for running commands that represents another interface to the user, and Package Registry - a registry for storing and downloading the specified packages, which will ideally use _IPFS_. The best analogy would perhaps be NPM, which also consists of the aforementioned parts (plus a website for users to monetize their tool :), and accordingly we named the tool SPM - Solidity Package Manager. The biggest challenges are: support for defining packages, autocomplete and intellisense options when writing a DSL script, defining a syntax that is understandable to programmers but also to people with less technical expertise, scanning local packages, and searching for existing packages in the registry (in our case, IPFS P2P network).

## Team Members

- [R2 21/2022 Albert Makan](https://github.com/albertmakan)
- [R2 23/2022 Miloš Panić](https://github.com/panicmilos)
- [R2 24/2022 Dragana Filipović](https://github.com/draganaf)
- [R2 27/2022 Luka Bjelica](https://github.com/bjelicaluka)
- [R2 40/2022 Nikola Petrović](https://github.com/nikolapetrovic1)

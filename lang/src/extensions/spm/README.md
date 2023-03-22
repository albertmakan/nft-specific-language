# Solidity Package Manager - Language Server 

This extension enables faster development of solidity packages. 

## Programming Languages and Frameworks

The extension template has two parts, the extension part and language server part. The extension part is written in TypeScript, and language server part is written in Python over the [_pygls_][pygls] (Python language server) library.

## Requirements

1. VS Code 1.64.0 or greater
1. Python 3.7 or greater (SPM, textX, jsonmerge)
1. node >= 14.19.0
1. npm >= 8.3.0 (`npm` is installed with node, check npm version, use `npm install -g npm@8.3.0` to update)
1. Python extension for VS Code

You should know to create and work with python virtual environments.

## Getting Started

1. [Everything you need to know is in documentation](https://spm.bjelicaluka.com/)

## Features of this Extension

1. Syntax highlight
1. Code snippets - init, package, using and @
1. Definition referencing
1. Syntax and semantic code validation
1. Code completion

## Building and Run the extension

Run the `Debug Extension and Python` configuration form VS Code. That should build and debug the extension in host window.

Note: if you just want to build you can run the build task in VS Code (`ctrl`+`shift`+`B`)

## Debugging

To debug both TypeScript and Python code use `Debug Extension and Python` debug config. This is the recommended way. Also, when stopping, be sure to stop both the Typescript, and Python debug sessions. Otherwise, it may not reconnect to the python session.

To debug only TypeScript code, use `Debug Extension` debug config.

To debug a already running server or in production server, use `Python Attach`, and select the process that is running `lsp_server.py`.
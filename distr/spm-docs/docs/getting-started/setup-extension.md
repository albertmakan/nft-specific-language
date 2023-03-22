---
sidebar_label: VSCode extension
sidebar_position: 2
---

# Setup SPM VSCode extension

In order to improve the development experience when working with `SPM` language, we've prepared a Visual Studio Code extension.

Extension can be found [here](https://marketplace.visualstudio.com/items?itemName=Siithub.spm).

Or you can find it by searching `SPM` in Visual Studio Code's extensions.

![An image from the static](/img/extension.png)

# Features of this Extension

1. Syntax highlight
2. Code snippets - init, package, using and @
3. Definition referencing
4. Syntax and semantic code validation
5. Code completion

# Building and Run the extension

Run the Debug Extension and Python configuration form VS Code. That should build and debug the extension in host window.

:::note
If you just want to build you can run the build task in VS Code (ctrl+shift+B).
:::

# Debugging

To debug both TypeScript and Python code use Debug Extension and Python debug config. This is the recommended way. Also, when stopping, be sure to stop both the Typescript, and Python debug sessions. Otherwise, it may not reconnect to the python session.

To debug only TypeScript code, use Debug Extension debug config.

To debug a already running server or in production server, use Python Attach, and select the process that is running lsp_server.py.

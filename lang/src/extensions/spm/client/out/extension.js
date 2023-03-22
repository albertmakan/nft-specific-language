"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const net = require("net");
const path = require("path");
const vscode_1 = require("vscode");
const node_1 = require("vscode-languageclient/node");
let client;
function getClientOptions() {
    return {
        // Register the server for plain text documents
        documentSelector: [
            { scheme: "file", language: "spm" },
            { scheme: "untitled", language: "spm" },
        ],
        outputChannelName: "[pygls] SpmLanguageServer",
        synchronize: {
            // Notify the server about file changes to '.clientrc files contain in the workspace
            fileEvents: vscode_1.workspace.createFileSystemWatcher("**/.clientrc"),
        },
    };
}
function startLangServerTCP(port) {
    const serverOptions = () => {
        return new Promise((resolve /*, reject */) => {
            const clientSocket = new net.Socket();
            clientSocket.connect(port, "127.0.0.1", () => {
                resolve({
                    reader: clientSocket,
                    writer: clientSocket,
                });
            });
        });
    };
    return new node_1.LanguageClient(`tcp lang server (port ${port})`, serverOptions, getClientOptions());
}
function startLangServer(command, args, cwd) {
    const serverOptions = {
        args,
        command,
        options: { cwd },
    };
    return new node_1.LanguageClient(command, serverOptions, getClientOptions());
}
function activate(context) {
    if (context.extensionMode === vscode_1.ExtensionMode.Development) {
        // Development - Run the server manually
        client = startLangServerTCP(2087);
    }
    else {
        // Production - Client is going to run the server (for use within `.vsix` package)
        const cwd = path.join(__dirname, "..", "..");
        const pythonPath = vscode_1.workspace
            .getConfiguration("python")
            .get("pythonPath");
        if (!pythonPath) {
            throw new Error("`python.pythonPath` is not set");
        }
        client = startLangServer(pythonPath, ["-m", "server"], cwd);
    }
    context.subscriptions.push(client.start());
}
exports.activate = activate;
function deactivate() {
    return client ? client.stop() : Promise.resolve();
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map
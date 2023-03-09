############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import asyncio
import json
import re
import time
import uuid
from json import JSONDecodeError
import os

from lsprotocol.types import (TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_CHANGE,
                              TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN,
                              TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
                              TEXT_DOCUMENT_DEFINITION)
from lsprotocol.types import (CompletionItem, CompletionList, CompletionOptions,

                              CompletionItemKind,
                              Location,
                              CompletionParams, ConfigurationItem,
                              Diagnostic,
                              DidChangeTextDocumentParams,
                              DidCloseTextDocumentParams,
                              DefinitionParams,
                              DidOpenTextDocumentParams, MessageType, Position,
                              Range, Registration, RegistrationParams,
                              SemanticTokens, SemanticTokensLegend, SemanticTokensParams,
                              Unregistration, UnregistrationParams,
                              WorkDoneProgressBegin, WorkDoneProgressEnd,
                              WorkDoneProgressReport,
                              WorkspaceConfigurationParams)
from pygls.server import LanguageServer

from server.sol_file_utils import extract_solidity_data_from_file

COUNT_DOWN_START_IN_SECONDS = 10
COUNT_DOWN_SLEEP_IN_SECONDS = 1


class SpmLanguageServer(LanguageServer):
    CMD_COUNT_DOWN_BLOCKING = 'countDownBlocking'
    CMD_COUNT_DOWN_NON_BLOCKING = 'countDownNonBlocking'
    CMD_PROGRESS = 'progress'
    CMD_REGISTER_COMPLETIONS = 'registerCompletions'
    CMD_SHOW_CONFIGURATION_ASYNC = 'showConfigurationAsync'
    CMD_SHOW_CONFIGURATION_CALLBACK = 'showConfigurationCallback'
    CMD_SHOW_CONFIGURATION_THREAD = 'showConfigurationThread'
    CMD_UNREGISTER_COMPLETIONS = 'unregisterCompletions'

    CONFIGURATION_SECTION = 'spmServer'

    def __init__(self, *args):
        super().__init__(*args)


spm_server = SpmLanguageServer('spm-language-support', 'v0.1')


def _validate(ls, params):
    ls.show_message_log('Validating spm...')

    text_doc = ls.workspace.get_document(params.text_document.uri)

    source = text_doc.source
    diagnostics = _validate_spm(source) if source else []

    ls.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_spm(source):
    """Validates spm file."""
    diagnostics = []

    try:
        json.loads(source)
    except JSONDecodeError as err:
        msg = "pera sisa"
        col = 1
        line = 2

        d = Diagnostic(
            range=Range(
                start=Position(line=line - 1, character=col - 1),
                end=Position(line=line - 1, character=col)
            ),
            message=msg,
            source=type(spm_server).__name__
        )

        diagnostics.append(d)

    return diagnostics

def _extract_base_file_path(uri: str):
    uri_tokens = uri.split('/')
    return '/'.join(uri_tokens[:-1])


local_packages = None
package_definitions = {}
solidity_files = {}


def load_local_packages():
    global local_packages
    if local_packages is not None:
        return

    package_json_path = os.path.join(
        spm_server.workspace.root_path, "package.json")
    with open(package_json_path, "r") as fp:
        package_json = json.loads(fp.read())
        if "packages" in package_json:
            local_packages = package_json["packages"]


def get_package_definition(package_name):

    if package_name in package_definitions:
        return package_definitions[package_name]

    if not package_name in local_packages:
        return None

    package_version = local_packages[package_name]

    package_path = os.path.join(spm_server.workspace.root_path,
                                "spm_packages", f"{package_name}_{package_version}.json")
    with open(package_path, "r") as fp:
        package = json.loads(fp.read())
        if "definition" in package:
            package_definition = package["definition"]
            package_definitions[package_name] = package_definition

            return package_definition


def get_solidity_file(solidity_file):
    if solidity_file in solidity_files:
        return solidity_files[solidity_file]

    sol_data = extract_solidity_data_from_file(solidity_file)
    solidity_files[solidity_file] = sol_data

    return sol_data


def form_auto_complition_response(suggestions: list[str], suggestion_kind=CompletionItemKind.Folder):
    items = [CompletionItem(label=suggestion, kind=suggestion_kind, sort_text=chr(
        0) + suggestion.lower()) for suggestion in suggestions]
    return CompletionList(
        is_incomplete=False,
        items=items,
    )


WHITE_SPACE = re.compile("^.*\s+")

USING_REGEX = re.compile("^using\s+")
USING_FILE_IMPORT_REGEX = re.compile("^using\s+\"")
USING_PACKAGE_IMPORT_REGEX = re.compile("^using\s+")

ALIAS_REGEX = re.compile("\s+as\s+")
HAS_ALIAS_REGEX = re.compile("^.*\s+as\s+.*")

EXPORT_TYPE_REGEX = re.compile("@(function|modifier|struct|contract|event)\s*")

IMPORT_REGEX = re.compile("[a-zA-Z0-9_.-]*")
DEFINITION_REGEX = re.compile("^using\s+[a-zA-Z0-9_.-]*\s+as\s+([a-zA-Z0-9_.-]*)")

def find_possible_file_imports(uri, current_input):
    inputed_path = re.sub(USING_FILE_IMPORT_REGEX, '',
                          current_input).replace('"', '')

    path = os.path.join(_extract_base_file_path(
        uri), _extract_base_file_path(inputed_path)) + "/"

    first_char = "/" if inputed_path.endswith('.') else ""
    return [first_char + f.path.replace(path, '') for f in os.scandir(path) if f.is_dir() or f.path.endswith(".sol")]


def find_possible_package_imports(current_input):
    inputed_path = re.sub(USING_PACKAGE_IMPORT_REGEX, '', current_input)

    package_tokens = inputed_path.split('.')
    if len(package_tokens) == 1:
        return local_packages.keys()

    package_name = package_tokens[0]
    package_definition = get_package_definition(package_name)
    if package_definition is None:
        return []

    current_package = package_definition
    for package_token in package_tokens[:-1]:
        current_package = current_package[package_token]

    return [key for key in current_package.keys() if "type" not in current_package[key] and "path" not in current_package[key]]


def find_aliasses(doc_lines):
    aliasses = {}

    # TODO: DUPLICATE ALIASSES
    for line in doc_lines:
        line = line.strip()
        if not USING_REGEX.match(line):
            continue

        line = re.sub(USING_REGEX, '', line).replace('"', '')
        aliasses[extract_alias(line)] = extract_package(line)

    return aliasses


def extract_package(line):
    if HAS_ALIAS_REGEX.match(line):
        return re.sub(ALIAS_REGEX, ' as ', line).split(' as ')[0]

    return line


def extract_alias(line):
    if HAS_ALIAS_REGEX.match(line):
        return re.sub(ALIAS_REGEX, ' as ', line).split(' as ')[-1]

    if line.endswith(".sol"):
        return line.split('/')[-1].replace(".sol", "")

    return line.split('.')[-1]


def find_suggestion_from_package(current_line, package_alias, package):
    current_input = current_line.replace(f'{package_alias}.', f'{package}.')

    package_name = package.split('.')[0]
    package_definition = get_package_definition(package_name)
    package_namespace_parts = current_input.split('.')

    current_package = package_definition
    for package_token in package_namespace_parts[:-1]:
        current_package = current_package[package_token]

    return [key for key in current_package.keys() if key not in ["path", "type"]]


@spm_server.feature(TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=['.', '/', '"', '@']))
def on_completion(ls: LanguageServer, params: CompletionParams) -> CompletionList:
    """Completion suggestions for character names."""

    # TODO: NAPRAVITI NACIN DA NADJEMO JESMO LI U PACKAGE ILI NE

    # load document
    uri = params.text_document.uri.replace('file://', '')
    doc = ls.workspace.get_document(params.text_document.uri)
    current_line = doc.lines[params.position.line].strip()
    current_col = params.position.character

    current_input = current_line[:current_col + 1]
    ls.show_message_log(current_input)

    load_local_packages()
    aliasses = find_aliasses(doc.lines)

    if USING_FILE_IMPORT_REGEX.match(current_line):
        possible_imports = find_possible_file_imports(uri, current_input)

        return form_auto_complition_response(possible_imports)

    if USING_PACKAGE_IMPORT_REGEX.match(current_line):
        possible_imports = find_possible_package_imports(current_input)

        return form_auto_complition_response(possible_imports)

    if current_line.startswith('@') and not WHITE_SPACE.match(current_line) and not EXPORT_TYPE_REGEX.match(current_line):
        return form_auto_complition_response(['function', 'struct', 'contract', 'modifier', 'event'], CompletionItemKind.Class)

    # ponudi aliase pa onda dalje
    should_suggest_aliasses = '.' not in current_line
    if should_suggest_aliasses:
        return form_auto_complition_response(aliasses.keys())

    current_line = re.sub(EXPORT_TYPE_REGEX, '', current_line)
    package_alias = current_line.split('.')[0]
    package = aliasses[package_alias]

    should_suggest_from_package = '.sol' not in package
    if should_suggest_from_package:
        suggestion = find_suggestion_from_package(
            current_line, package_alias, package)
        return form_auto_complition_response(suggestion)

    suggestion = find_suggestions_from_file(uri, current_line, package)

    return form_auto_complition_response(suggestion)


def find_suggestions_from_file(uri, current_line, package):
    sol_file_path = f'"{os.path.join(_extract_base_file_path(uri), package)}"'
    sol_data = get_solidity_file(sol_file_path)

    export_tokens = current_line.split('.')
    if len(export_tokens) not in [2, 3]:
        return []

    if len(export_tokens) == 2:
        return get_first_depth_suggestions_from_file(sol_data)

    contract = export_tokens[1]
    return get_second_depth_suggestions_from_file(sol_data, contract)


def get_first_depth_suggestions_from_file(sol_data):

    contract_names = [contract for contract in sol_data.keys()
                      if contract != '@global']

    global_exports = get_exports_from_contract(sol_data, '@global')
    contract_names.extend(global_exports)

    return contract_names


def get_second_depth_suggestions_from_file(sol_data, contract):

    if contract not in sol_data:
        return []

    return get_exports_from_contract(sol_data, contract)


def get_exports_from_contract(sol_data, contract):

    exports = []
    inheritance_chain = [contract]

    while len(inheritance_chain):
        current_contract = inheritance_chain.pop()
        contract_data = sol_data[current_contract]

        if "base" in contract_data and contract_data["base"] is not None:
            inheritance_chain.append(contract_data["base"])

        for sol_type, sol_type_data in contract_data.items():
            if sol_type in ["base", "code", "variables", "imports"]:
                continue

            exports.extend(sol_type_data.keys())

    return exports


@spm_server.feature(TEXT_DOCUMENT_DEFINITION)
def find_reference(ls, params: DefinitionParams):

    uri = params.text_document.uri
    document = ls.workspace.get_document(uri)
    origin_pos = params.position
    origin_line = origin_pos.line
    origin_varname = document.word_at_position(origin_pos)

    for i in range(1,origin_line+1):
        current_line = document.lines[i].strip()
        match_import = re.match(DEFINITION_REGEX,current_line)
        if match_import and match_import.group(1) == origin_varname:
            definition_start = document.lines[i].find(origin_varname)
            definition_end = definition_start + len(origin_varname)    
            target_range = Range(start = Position(line=i,character=definition_start),end=Position(line=i,character=definition_end))
            return Location(uri=uri,range=target_range)
    return None

@spm_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    # _validate(ls, params)


@spm_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: SpmLanguageServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message('Text Document Did Close')


@spm_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message('Text Document Did Open')
    _validate(ls, params)


@spm_server.feature(
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    SemanticTokensLegend(
        token_types=["operator"],
        token_modifiers=[]
    )
)
def semantic_tokens(ls: SpmLanguageServer, params: SemanticTokensParams):
    """See https://microsoft.github.io/language-server-protocol/specification#textDocument_semanticTokens
    for details on how semantic tokens are encoded."""

    TOKENS = re.compile('".*"(?=:)')

    uri = params.text_document.uri
    doc = ls.workspace.get_document(uri)

    last_line = 0
    last_start = 0

    data = []

    for lineno, line in enumerate(doc.lines):
        last_start = 0

        for match in TOKENS.finditer(line):
            start, end = match.span()
            data += [
                (lineno - last_line),
                (start - last_start),
                (end - start),
                0,
                0
            ]

            last_line = lineno
            last_start = start

    return SemanticTokens(data=data)


@spm_server.command(SpmLanguageServer.CMD_PROGRESS)
async def progress(ls: SpmLanguageServer, *args):
    """Create and start the progress on the client."""
    token = str(uuid.uuid4())
    # Create
    await ls.progress.create_async(token)
    # Begin
    ls.progress.begin(token, WorkDoneProgressBegin(
        title='Indexing', percentage=0))
    # Report
    for i in range(1, 10):
        ls.progress.report(
            token,
            WorkDoneProgressReport(message=f'{i * 10}%', percentage=i * 10),
        )
        await asyncio.sleep(2)
    # End
    ls.progress.end(token, WorkDoneProgressEnd(message='Finished'))


@spm_server.command(SpmLanguageServer.CMD_REGISTER_COMPLETIONS)
async def register_completions(ls: SpmLanguageServer, *args):
    """Register completions method on the client."""
    params = RegistrationParams(registrations=[
        Registration(
            id=str(uuid.uuid4()),
            method=TEXT_DOCUMENT_COMPLETION,
            register_options={"triggerCharacters": "[':']"})
    ])
    response = await ls.register_capability_async(params)
    if response is None:
        ls.show_message('Successfully registered completions method')
    else:
        ls.show_message('Error happened during completions registration.',
                        MessageType.Error)


@spm_server.command(SpmLanguageServer.CMD_SHOW_CONFIGURATION_ASYNC)
async def show_configuration_async(ls: SpmLanguageServer, *args):
    """Gets exampleConfiguration from the client settings using coroutines."""
    try:
        config = await ls.get_configuration_async(
            WorkspaceConfigurationParams(items=[
                ConfigurationItem(
                    scope_uri='',
                    section=SpmLanguageServer.CONFIGURATION_SECTION)
            ]))

        example_config = config[0].get('exampleConfiguration')

        ls.show_message(
            f'spmServer.exampleConfiguration value: {example_config}')

    except Exception as e:
        ls.show_message_log(f'Error ocurred: {e}')


@spm_server.command(SpmLanguageServer.CMD_SHOW_CONFIGURATION_CALLBACK)
def show_configuration_callback(ls: SpmLanguageServer, *args):
    """Gets exampleConfiguration from the client settings using callback."""
    def _config_callback(config):
        try:
            example_config = config[0].get('exampleConfiguration')

            ls.show_message(
                f'spmServer.exampleConfiguration value: {example_config}')

        except Exception as e:
            ls.show_message_log(f'Error ocurred: {e}')

    ls.get_configuration(
        WorkspaceConfigurationParams(
            items=[
                ConfigurationItem(
                    scope_uri='',
                    section=SpmLanguageServer.CONFIGURATION_SECTION)
            ]
        ),
        _config_callback
    )


@spm_server.thread()
@spm_server.command(SpmLanguageServer.CMD_SHOW_CONFIGURATION_THREAD)
def show_configuration_thread(ls: SpmLanguageServer, *args):
    """Gets exampleConfiguration from the client settings using thread pool."""
    try:
        config = ls.get_configuration(WorkspaceConfigurationParams(items=[
            ConfigurationItem(
                scope_uri='',
                section=SpmLanguageServer.CONFIGURATION_SECTION)
        ])).result(2)

        example_config = config[0].get('exampleConfiguration')

        ls.show_message(
            f'spmServer.exampleConfiguration value: {example_config}')

    except Exception as e:
        ls.show_message_log(f'Error ocurred: {e}')



import json
import re
import os
from spm import language_server
from textx import TextXSyntaxError
from lsprotocol.types import (TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_CHANGE,
                              TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN,
                              TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
                              TEXT_DOCUMENT_DEFINITION)
from lsprotocol.types import (CompletionItem, CompletionList, CompletionOptions,\
                              CompletionItemKind,
                              Location,
                              CompletionParams, ConfigurationItem,
                              Diagnostic,DiagnosticSeverity,
                              DidChangeTextDocumentParams,
                              DidCloseTextDocumentParams,
                              DefinitionParams,
                              DidOpenTextDocumentParams, MessageType, Position,
                              Range, Registration, RegistrationParams,
                              SemanticTokens, SemanticTokensLegend, SemanticTokensParams,
)
from pygls.server import LanguageServer
from server.regexs import (USING_FILE_IMPORT_REGEX, USING_PACKAGE_IMPORT_REGEX, USING_REGEX, HAS_ALIAS_REGEX, ALIAS_REGEX, WHITE_SPACE, EXPORT_TYPE_REGEX, DEFINITION_REGEX)

from server.sol_file_utils import extract_solidity_data_from_file
from server.completion_utils import form_auto_complition_response, find_possible_file_imports
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

mm = language_server.create_mm()

def load_local_packages(doc = None):
    try:
        package_json_path = os.path.join(spm_server.workspace.root_path, "package.json")
        with open(package_json_path, "r") as fp:
            package_json = json.loads(fp.read())
            if "packages" in package_json:
                return package_json["packages"]
        return {}
    except:
        d = Diagnostic(
        range=Range(
            start=Position(line=0, character=0),
            end=Position(line=0, character=0),
        ),
        message="package.json not found",
        source=type(spm_server).__name__,
        severity=DiagnosticSeverity.Warning)
        spm_server.publish_diagnostics(doc.uri,[d])
        return {}



def create_diagnostic(err):
    msg = err.message
    col = err.col
    line = err.line
    d = Diagnostic(
        range=Range(
            start=Position(line=line - 1, character=0),
            end=Position(line=line - 1, character=80),
        ),
        message=msg,
        source=type(spm_server).__name__,
        severity=DiagnosticSeverity.Error
    )
    return d

def _validate(ls:SpmLanguageServer, params):

    text_doc = ls.workspace.get_document(params.text_document.uri)
    source = text_doc.source

    language_server.change_packages(load_local_packages(text_doc))
    language_server.change_path(ls.workspace.root_path)
    diagnostics = _validate_spm(source) if source else []
    ls.publish_diagnostics(text_doc.uri, diagnostics)

def _validate_spm(source):
    """Validates spm file."""
    diagnostics = []
    try:
        #syntax
        model = mm.model_from_str(source)
    except TextXSyntaxError as err:
        diagnostics.append(create_diagnostic(err))
        return diagnostics
    #semantics
    if "errors" in dir(model):
        for err in model.errors:
            diagnostics.append(create_diagnostic(err))
    return diagnostics




def _extract_base_file_path(uri: str):
    uri_tokens = uri.split('/')
    return '/'.join(uri_tokens[:-1])


local_packages = None
package_definitions = {}
solidity_files = {}


def set_local_packages(doc = None):
    global local_packages
    if local_packages is not None:
        return
    if local_packages and len(local_packages):
        return
    local_packages = load_local_packages(doc)

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

    set_local_packages(params.text_document)
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
            inheritance_chain.extend(contract_data["base"])

        for sol_type, sol_type_data in contract_data.items():
            if sol_type in ["base", "code", "variables", "imports"]:
                continue

            exports.extend(sol_type_data.keys())

    return exports


@spm_server.feature(TEXT_DOCUMENT_DEFINITION)
def find_reference(ls:LanguageServer, params: DefinitionParams):
    uri = params.text_document.uri
    document = ls.workspace.get_document(uri)
    origin_pos = params.position
    origin_line = origin_pos.line
    origin_varname = document.word_at_position(origin_pos)

    for i in range(1,origin_line+1):
        current_line = document.lines[i].strip()
        match_import = re.match(DEFINITION_REGEX,current_line)
        if match_import and (match_import.group(1) == origin_varname or match_import.group(2) == origin_varname):
            definition_start = document.lines[i].find(origin_varname)
            definition_end = definition_start + len(origin_varname)    
            target_range = Range(start = Position(line=i,character=definition_start),end=Position(line=i,character=definition_end))
            return Location(uri=uri,range=target_range)
    return None

@spm_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _validate(ls, params)


# @spm_server.feature(TEXT_DOCUMENT_DID_CLOSE)
# def did_close(server: SpmLanguageServer, params: DidCloseTextDocumentParams):
#     """Text document did close notification."""
#     server.show_message('Text Document Did Close')


@spm_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    #TODO: proslediti path ka package.json ls.workspace.root_path
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

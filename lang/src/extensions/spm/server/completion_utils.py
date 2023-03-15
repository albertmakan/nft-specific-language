from lsprotocol.types import (CompletionItem, CompletionItemKind, CompletionList)
from server.regexs import USING_FILE_IMPORT_REGEX
import re
import os
def form_auto_complition_response(suggestions: list[str], suggestion_kind=CompletionItemKind.Folder):
    items = [CompletionItem(label=suggestion, kind=suggestion_kind, sort_text=chr(
        0) + suggestion.lower()) for suggestion in suggestions]
    return CompletionList(
        is_incomplete=False,
        items=items,
    )


def _extract_base_file_path(uri: str):
    uri_tokens = uri.split('/')
    return '/'.join(uri_tokens[:-1])

def find_possible_file_imports(uri, current_input):
    inputed_path = re.sub(USING_FILE_IMPORT_REGEX, '',
                          current_input).replace('"', '')

    path = os.path.join(_extract_base_file_path(
        uri), _extract_base_file_path(inputed_path)) + "/"

    first_char = "/" if inputed_path.endswith('.') else ""
    return [first_char + f.path.replace(path, '') for f in os.scandir(path) if f.is_dir() or f.path.endswith(".sol")]


import re

WHITE_SPACE = re.compile("^.*\s+")

USING_REGEX = re.compile("^using\s+")

USING_FILE_IMPORT_REGEX = re.compile("^using\s+\"")

USING_PACKAGE_IMPORT_REGEX = re.compile("^using\s+")

ALIAS_REGEX = re.compile("\s+as\s+")
HAS_ALIAS_REGEX = re.compile("^.*\s+as\s+.*")

EXPORT_TYPE_REGEX = re.compile("@(function|modifier|struct|contract|event)\s*")

IMPORT_REGEX = re.compile("[a-zA-Z0-9_.-]*")
DEFINITION_REGEX = re.compile("^using\s+([a-zA-Z0-9_.-]*)\s+as\s+([a-zA-Z0-9_.-]*)")
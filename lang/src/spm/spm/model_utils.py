from .model import Script, Construct, PackageImport, PackageExport
from .file_utils import is_file


def find_root(construct: Construct) -> Script:
    c: Construct = construct
    while True:
        if 'parent' not in dir(c):
            break
        c = c.parent
        
    return c

def find_import(package_export: PackageExport) -> PackageImport:
    root = find_root(package_export)
    package_alias = package_export.export_name.split('.')[0]

    for imported_package in root.imports.packages:
        if imported_package.alias == package_alias:
            return imported_package


def compute_package_alias(package: PackageImport):
    if (package.alias):
        return package.alias

    isFileImport = is_file(package.id)
    if isFileImport:
        return package.id.replace('"', '').split('/')[-1].replace('.sol', '')
    
    return package.id.split('.')[-1]

def compute_exported_name(export: PackageExport):
    if export.package_name:
        return export.package_name

    if export.export_alias:
        return export.export_alias

    return export.export_name.split('.')[-1]
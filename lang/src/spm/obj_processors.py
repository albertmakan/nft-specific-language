from typing import List
from model import Construct, PackageExport, PackageExportSection, PackageImportSection, PackageImport, Script
from os import path

from sol_code_extractions import extract_sol_data
from sol_dependency_analysers import form_dependencies
from merge import merge


solidity_files = { }

def package_import_section_processor(package_section: PackageImportSection):
    names = []
    for pack in package_section.packages:
        if not pack.alias:
            pack.alias = _compute_pack_alias(pack)
        if pack.alias in names:
            raise Exception(f"Multiple imports with same name: '{pack.alias}'")
        names.append(pack.alias)

def _compute_pack_alias(pack: PackageImport):
    isFileImport = _is_file_import(pack.id)
    if isFileImport:
        return pack.id.replace('"', '').split('/')[-1].replace('.sol', '')
    
    return pack.id.split('.')[-1]

def package_import_processor(package_import: PackageImport):

    isFileImport = _is_file_import(package_import.id)
    if isFileImport:
        _check_file_path(package_import.id)

        input, input_lines = _load_solidity_file(package_import.id)

        sol_data = extract_sol_data(input, input_lines)
        dependencies = form_dependencies(sol_data)
        merged_sol_data = merge(sol_data, dependencies)

        solidity_files[package_import.alias] = merged_sol_data
        package_import.data = merged_sol_data


def _is_file_import(id):
    return id.startswith('".') and id.endswith('"')

def _check_file_path(filePath):
    if not path.isfile(filePath.replace('"', '')):
        raise Exception(f"{filePath} is not correct file path")

def _load_solidity_file(file_path):
  with open(file_path.replace('"', ''), "r") as fp:
    input = fp.read()
    fp.seek(0)
    input_lines = fp.readlines()

    return input, input_lines

def package_export_section_processor(package_section: PackageExportSection):
    process_ambiguous_exports(package_section.exports)

    print_package_export_section(package_section)

def process_ambiguous_exports(exports: List[PackageExport]):
    try_to_find_ambiguous_export(exports)
    for export in exports:
        if not export.exports:
            continue
        process_ambiguous_exports(export.exports)
    
def try_to_find_ambiguous_export(exports: List[PackageExport]):
    defined_names = []
    for export in exports:
        name = _compute_exported_name(export)

        if name in defined_names:
            raise Exception(f"{name} is already defined")

        defined_names.append(name)

def _compute_exported_name(export: PackageExport):
    if export.package_name:
        return export.package_name

    if export.export_alias:
        return export.export_alias

    return export.export_name.split('.')[-1]

def package_export_processor(export: PackageExport):
    if export.package_name:
        return
    if not export.export_type:
        export.export_type = '@function'

    export_name_tokens = export.export_name.split('.')

    if len(export_name_tokens) != 2 and export.export_type == '@contract':
        raise Exception(f"Export for contract must be PackageAlias.ContractName")

    if len(export_name_tokens) != 3 and export.export_type == '@event':
        raise Exception(f"Export for event must be PackageAlias.ContractName.EventName")

    if len(export_name_tokens) not in [2, 3]:
        raise Exception(f"Export must be PackageAlias[.ContractName].SolidityTypeName")
    
    _check_if_package_is_imported(export, export_name_tokens[0])

    if export.export_type == '@contract':
        _check_if_contract_exists(export)
    if export.export_type in ['@function', '@struct', '@event']:
        _check_if_non_contract_exists(export)


def _check_if_contract_exists(export: PackageExport):
    export_name_tokens = export.export_name.split('.')
    _check_if_contract_exists_in_package(export_name_tokens[0], export_name_tokens[1])

def _check_if_non_contract_exists(export: PackageExport):
    export_name_tokens = export.export_name.split('.')
    if len(export_name_tokens) == 2:
        _check_if_solidity_type_exists_in_package(export_name_tokens[0], '@global', export.export_type, export_name_tokens[1])

    if len(export_name_tokens) == 3:
        _check_if_contract_exists_in_package(export_name_tokens[0], export_name_tokens[1])
        _check_if_solidity_type_exists_in_package(export_name_tokens[0], export_name_tokens[1], export.export_type, export_name_tokens[2])


def _check_if_package_is_imported(export: PackageExport, package_alias: str):
    root = _find_root(export)
    if not root:
        raise Exception("No root")

    pack = next((package for package in root.imports.packages if package.alias == package_alias), None)
    if not pack:
        raise Exception(f"Package '{package_alias}' not found")
    # method.name = pack.id + (('.' + p[-1]) if len(p)>1 else '')

def _check_if_contract_exists_in_package(package_alias: str, contract_name: str):
    if contract_name not in solidity_files[package_alias]:
        raise Exception(f"Contract '{contract_name}' not found in package '{package_alias}'")

def _check_if_solidity_type_exists_in_package(package_alias: str, contract_name: str, export_type: str, export_name: str):
    export_type = export_type.replace('@', '') + 's'
    if export_name not in solidity_files[package_alias][contract_name][export_type]:
        raise Exception(f"{export_type[:-1]} '{export_name}' not found in contract '{contract_name}' of '{package_alias}' package")



def print_package_export_section(package_section: PackageExportSection):
    print("Main package: " + package_section.name)
    for export in package_section.exports:
        print_package_export(export)


def print_package_export(export: PackageExport):
    if export.export_name:
        if not export.export_type:
            export.export_type = '@function'
        print(export.export_type + ": " + export.export_name)
        return

    print("Nested package: " + export.package_name)
    for nested_export in export.exports:
        print_package_export(nested_export)


def _find_root(construct: Construct) -> Script:
    c: Construct = construct
    while True:
        if 'parent' not in dir(c):
            break
        c = c.parent
        
    return c
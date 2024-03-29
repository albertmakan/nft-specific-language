import os
from typing import List
import jsonmerge

from .constants import *
from .errors import raise_error, errorHandlerWrapper
from .model import PackageExport, PackageExportSection, PackageImportSection, PackageImport
from .sol_code_extractions import extract_sol_data
from .sol_dependency_analysers import form_dependencies, find_contract_chain
from .file_utils import load_local_packages, load_solidity_file, load_package, check_file_path, is_file
from .model_utils import find_import, compute_package_alias, compute_exported_name


solidity_files = {}
local_packages = None
base_path = ''

def get_local_packages():
    global local_packages
    if local_packages is None:
        local_packages = load_local_packages()

    return local_packages

def change_local_packages(packages):
    global local_packages
    local_packages = packages

def change_base_path(path):
    global base_path
    base_path = path

# -------------------- PACKAGE IMPORT SECTION PROCESSOR --------------------

@errorHandlerWrapper()
def package_import_section_processor(package_section: PackageImportSection):
    names = []
    for package in package_section.packages:
        if package.alias in names:
            raise_error(f"Multiple imports with same name: '{package.alias}'", package)
        names.append(package.alias)

# ------------------------ PACKAGE IMPORT PROCESSOR -------------------------

@errorHandlerWrapper()
def package_import_processor(package_import: PackageImport):
    package_import.alias = compute_package_alias(package_import)

    isFileImport = is_file(package_import.id)
    if isFileImport:
        process_imported_solidity_file(package_import)
        return
    
    process_imported_spm_package(package_import)


def process_imported_solidity_file(package_import: PackageImport):
    sol_data = {}
    load_queue = [package_import.id]

    while len(load_queue):
        file_path = load_queue.pop()
        isFileImport = is_file(file_path)
        if isFileImport:
            if base_path:
                file_path = '"' + os.path.join(base_path, file_path.replace('"', '')) + '"'

            check_file_path(file_path)

            input = load_solidity_file(file_path)
            file_sol_data = extract_sol_data(input)
            
            sol_data = jsonmerge.merge(sol_data, file_sol_data)

            parent_file_path = os.path.dirname(file_path.replace('"', ''))
            for imported_file in file_sol_data[GLOBAL][IMPORTS]:
                if is_file(imported_file):
                    load_queue.append('"{0}"'.format(os.path.join(parent_file_path, imported_file.replace('"', ''))))

    # this is to remove interfaces
    for contract_data in sol_data.values():
        contract_data[BASE] = [name for name in contract_data[BASE] if name in sol_data]

    form_dependencies(sol_data)

    solidity_files[package_import.alias] = sol_data
    package_import.data = sol_data


def process_imported_spm_package(package_import: PackageImport):
    package_name = package_import.id.split(".")[0]
    _check_local_package(package_import, package_name)
    
    spm_modules_path = os.path.join(base_path, "spm_packages")
    package = load_package(package_name, get_local_packages()[package_name], spm_modules_path)
        
    _check_package_namespace(package_import, package, package_import.id)

    solidity_files[package_import.alias] = package
    package_import.data = package

def _check_local_package(package_import: PackageImport, package_name: str):
    if package_name not in get_local_packages():
        raise_error(f"{package_name} is not installed", package_import)

def _check_package_namespace(package_import, package, package_namespace):
    namespace_parts = package_namespace.split(".")
    package_name = namespace_parts[0]
    
    package_definition = package["definition"]
    current_package = package_definition
    for namespace_part in namespace_parts:
        if namespace_part not in current_package:
            raise_error(f"{package_namespace} namespace is not defined in {package_name} package", package_import)

        current_package = current_package[namespace_part]

        if 'type' in current_package and 'path' in current_package:
            raise_error(f"Solidity {current_package['type'][:-1]} {package_namespace} cannot be imported directly", package_import)

# -------------------- PACKAGE EXPORT SECTION PROCESSOR --------------------

@errorHandlerWrapper()
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
        name = compute_exported_name(export)

        if name in defined_names:
            raise_error(f"{name} is already defined", export)

        defined_names.append(name)

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

# ------------------------ PACKAGE EXPORT PROCESSOR -------------------------

@errorHandlerWrapper()
def package_export_processor(export: PackageExport):
    if export.export_name is None and len(export.exports) == 0:
        raise_error(f"Every namespace must have at least one export", export)
    
    if export.package_name:
        return
    
    if not export.export_type:
        export.export_type = '@function'

    imported_package = find_import(export)
    if imported_package is None:
        raise_error(f"Package '{export.export_name.split('.')[0]}' not found", export)

    if is_file(imported_package.id):
        process_export_from_file(export)
    else:
        process_export_from_package(imported_package, export)

def process_export_from_file(export: PackageExport):
    export_name_tokens = export.export_name.split('.')
    if len(export_name_tokens) != 2 and export.export_type == '@contract':
        raise_error(f"Export for contract must be PackageAlias.ContractName", export)

    if len(export_name_tokens) != 3 and export.export_type == '@event':
        raise_error(f"Export for event must be PackageAlias.ContractName.EventName", export)

    if len(export_name_tokens) != 3 and export.export_type == '@modifier':
        raise_error(f"Export for modifier must be PackageAlias.ContractName.ModifierName", export)

    if len(export_name_tokens) not in [2, 3]:
        raise_error(f"Export must be PackageAlias[.ContractName].SolidityTypeName", export)
    

    if export.export_type == '@contract':
        _check_if_contract_exists(export)
    if export.export_type in ['@function', '@struct', '@event', '@modifier']:
        _check_if_non_contract_exists(export)

def process_export_from_package(imported_package: PackageImport, export: PackageExport):
    full_export = "{0}.{1}".format(imported_package.id, export.export_name.replace(imported_package.alias + ".", ""))

    # check namespace up to last .
    namespace_parts, export_name = full_export.split(".")[:-1], full_export.split(".")[-1]
    package_name = namespace_parts[0]
    current_package = imported_package.data["definition"]
    for i, namespace_part in enumerate(namespace_parts):
        if namespace_part not in current_package:
            visided_namespace = '.'.join(namespace_parts[:i+1]) 
            raise_error(f"{visided_namespace} namespace is not defined in {package_name} package", export)
        current_package = current_package[namespace_part]

        if 'type' in current_package and 'path' in current_package:
            raise_error(f"Expected namespace but got solidity {namespace_part} {current_package['type'][:-1]} instead", export)

    # check export
    if export_name not in current_package:
        full_namespace = '.'.join(namespace_parts)
        raise_error(f"{export_name} does not exist in {full_namespace} namespace of {package_name} package", export)

    current_package = current_package[export_name]
    if 'type' not in current_package and 'path' not in current_package:
        raise_error(f"{export_name} is a part of a namespace and not the solidity type", export)

    if export.export_type != ('@' + current_package['type'][:-1]):
        raise_error(f"Expected {export_name} to be {export.export_type[1:]} but is {current_package['type'][:-1]}", export)


def _check_if_contract_exists(export: PackageExport):
    export_name_tokens = export.export_name.split('.')
    _check_if_contract_exists_in_package(export, export_name_tokens[0], export_name_tokens[1])

def _check_if_non_contract_exists(export: PackageExport):
    export_name_tokens = export.export_name.split('.')
    if len(export_name_tokens) == 2:
        _check_if_solidity_type_exists_in_package(export, export_name_tokens[0], '@global', export.export_type, export_name_tokens[1])

    if len(export_name_tokens) == 3:
        _check_if_contract_exists_in_package(export, export_name_tokens[0], export_name_tokens[1])
        _check_if_solidity_type_exists_in_package(export, export_name_tokens[0], export_name_tokens[1], export.export_type, export_name_tokens[2])

def _check_if_contract_exists_in_package(export: PackageExport, package_alias: str, contract_name: str):
    if contract_name not in solidity_files[package_alias]:
        raise_error(f"Contract '{contract_name}' not found in package '{package_alias}'", export)

def _check_if_solidity_type_exists_in_package(export: PackageExport, package_alias: str, contract_name: str, export_type: str, export_name: str):
    export_type = export_type.replace('@', '') + 's'
    if export_name in solidity_files[package_alias][contract_name][export_type]:
        return
    for current_contract_name in find_contract_chain(contract_name, solidity_files[package_alias]):
        if export_name in solidity_files[package_alias][current_contract_name][export_type]:
            return
    raise_error(f"{export_type[:-1]} '{export_name}' not found in contract '{contract_name}' of '{package_alias}' package", export)

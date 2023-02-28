import json
from typing import List
from textx import generator
from model import Script, PackageImport, PackageExport
from package_code_generator import generate_package_code, find_all_exported_items
from model_utils import find_import

__version__ = "0.1.0.dev"

@generator('spm', 'solidity')
def spm_generate_solidity(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating solidity from spm descriptions"

    # output_file = get_output_filename(model.file_name, output_path, '*.spm')
    # gen_file(model.file_name, output_file,
    #          partial(generator_callback, model, output_file),
    #          overwrite,
    #          success_message='To convert to png run "dot -Tpng -O {}"'
    #          .format(os.path.basename(output_file)))
    output_file="proba-spm"
    generator_callback(model, output_file, overwrite)

def generator_callback(model: Script, output_file: str, overwrite: bool):
    """
    A generator function that produce output_file from model.
    """

    package_output = { 
        'definition': {},
        'solidity_code': {}
    }
    exports_per_package = {}

    solidity_files = get_solidity_files_from_imports(model.imports.packages)
    package_definition = map_export_to_output(PackageExport(None, model.package.name, model.package.exports, None, None, None))
    extract_exports_per_packages(package_definition, exports_per_package)

    for package_alias, exports in exports_per_package.items():
        exports_and_dependencies = find_all_exported_items(solidity_files[package_alias], exports)
        package_output['solidity_code'][package_alias] = generate_package_code(solidity_files[package_alias], exports_and_dependencies)
    package_output['definition'] = package_definition

    with open(output_file, 'w') as f:
        f.write(json.dumps(package_output, sort_keys=True, indent=4))


def get_solidity_files_from_imports(packages: List[PackageImport]):

    solidity_files = {}
    for package_import in packages:
        if _is_file_import(package_import):
            solidity_files[package_import.alias] = package_import.data
        else:
            solidity_files.update({ "{0}+{1}".format(package_import.alias, subPackage) : subPackageData for subPackage, subPackageData in package_import.data["solidity_code"].items() })
    return solidity_files


def map_export_to_output(export: PackageExport):
    if not export.exports:
        package_import = find_import(export)
        if _is_file_import(package_import):
            return _map_export_from_file_to_output(export)
        
        return _map_export_from_package_to_output(package_import, export)

    output = { export.package_name: {} }
    for nested_export in export.exports:
        if nested_export.package_name:
            output[export.package_name][nested_export.package_name] = map_export_to_output(nested_export)[nested_export.package_name]
        else:
            alias, export_type, export_path = map_export_to_output(nested_export)
            output[export.package_name][alias] = {
                'type': export_type.replace('@', '') + 's',
                'path': export_path
            }

    return output

def _map_export_from_file_to_output(export: PackageExport):
    export_name_tokens = export.export_name.split('.')
    export_name = _compute_export_name(export)

    return export.export_alias if export.export_alias else export_name_tokens[-1], export.export_type, export_name

def _map_export_from_package_to_output(package_import: PackageImport, export: PackageExport):
        package_definition = package_import.data["definition"]
        full_export = package_import.id + "." + export.export_name.replace(package_import.alias + ".", "")
        namespace_parts = full_export.split(".")
        current_package = package_definition
        for namespace_part in namespace_parts:
            current_package = current_package[namespace_part]

        return export.export_alias if export.export_alias else namespace_parts[-1], export.export_type, package_import.alias + "+" + current_package["path"]

def _is_file_import(package_import: PackageImport):
    return 'definition' not in package_import.data and 'solidity_code' not in package_import.data

def _compute_export_name(export: PackageExport):
    export_name_tokens = export.export_name.split('.')
    if len(export_name_tokens) == 3 or export.export_type == '@contract':
        return export.export_name

    return '.'.join([export_name_tokens[0], '@global', export_name_tokens[1]])


def extract_exports_per_packages(output: dict, exports_per_package: dict):
    for value in output.values():
        if type(value) is not dict or ('type' in value and 'path' in value):
            export_name_tokens = value['path'].split('.')

            package_alias = export_name_tokens[0]
            if package_alias not in exports_per_package:
                exports_per_package[package_alias] = []

            export_name_tokens.append(value['type'])
            function_name = '.'.join(export_name_tokens[1:]) 
            if function_name not in exports_per_package[package_alias]:
                exports_per_package[package_alias].append(function_name)

        else:
            extract_exports_per_packages(value, exports_per_package)

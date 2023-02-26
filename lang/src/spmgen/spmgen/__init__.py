import json
import os
import pprint
from typing import List
from model import PackageExport
from package_code_generator import generate_package_code, find_all_exported_items
from textx import generator
from spm import Script
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
    solidity_files = { package_import.alias: package_import.data for package_import in model.imports.packages }

    package_definition = map_export_to_output(PackageExport(None, model.package.name, model.package.exports, None, None, None))
    extract_needed_exports(package_definition, exports_per_package)

    for package_alias, exports in exports_per_package.items():
        exports_and_dependencies = find_all_exported_items(solidity_files[package_alias], exports)
        package_output['solidity_code'][package_alias] = generate_package_code(solidity_files[package_alias], exports_and_dependencies)
    package_output['definition'] = package_definition

    with open(output_file, 'w') as f:
        f.write(json.dumps(package_output, sort_keys=True, indent=4))


def extract_needed_exports(output: dict, exports_per_package: dict):
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
            extract_needed_exports(value, exports_per_package)

def compute_export_name(export: PackageExport):
    export_name_tokens = export.export_name.split('.')
    if len(export_name_tokens) == 3 or export.export_type == '@contract':
        return export.export_name

    return '.'.join([export_name_tokens[0], '@global', export_name_tokens[1]])

def map_export_to_output(export: PackageExport):
    if not export.exports:
        export_name_tokens = export.export_name.split('.')
        export_name = compute_export_name(export)

        return export.export_alias if export.export_alias else export_name_tokens[-1], export.export_type, export_name

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

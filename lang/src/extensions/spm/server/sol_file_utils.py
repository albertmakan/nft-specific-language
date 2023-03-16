import os
from spm.sol_code_extractions import extract_sol_data
from spm.file_utils import load_solidity_file, check_file_path
from spm.merge import merge_data

def extract_solidity_data_from_file(sol_file_path):
    sol_data = {}
    load_queue = [sol_file_path]

    while len(load_queue):
        file_path = load_queue.pop()
        isFileImport = is_file(file_path)
        if isFileImport:
            check_file_path(file_path)

            input = load_solidity_file(file_path)

            file_sol_data = extract_sol_data(input)
            sol_data = merge_data(sol_data, file_sol_data)

            parent_file_path = os.path.dirname(file_path.replace('"', ''))
            for imported_file in file_sol_data['@global']['imports']:
                if is_file(imported_file):
                    load_queue.append('"{0}"'.format(os.path.join(
                        parent_file_path, imported_file.replace('"', ''))))

    # this is to remove interfaces
    for contract_data in sol_data.values():
        if contract_data['base'] and contract_data['base'] not in sol_data:
            contract_data['base'] = None

    return sol_data

def is_file(id):
    return id.startswith('"') and id.endswith('"')

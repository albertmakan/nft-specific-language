import json, time

from spm.file_utils import load_solidity_file
from spm.merge import merge_data_with_dependencies
from spm.sol_code_extractions import extract_sol_data 
from spm.sol_dependency_analysers import form_dependencies
# from package_generator import find_all_exported_items, generate_package


if __name__ == "__main__":
  input = load_solidity_file("./ERC20.sol")

  start = time.time()

  sol_data = extract_sol_data(input)
  dependencies = form_dependencies(sol_data)
  merged_sol_data = merge_data_with_dependencies(sol_data, dependencies)
  # exported_items = find_all_exported_items(merged_sol_data, ['ERC20.transfer'])
  # package = generate_package(merged_sol_data, exported_items)

  with open("./output.json", "w") as fp:
    fp.write(json.dumps(sol_data, sort_keys=True, indent=4))

  with open("./dependencies.json", "w") as fp:
    fp.write(json.dumps(dependencies, sort_keys=True, indent=4))

  with open("./output_merged.json", "w") as fp:
    fp.write(json.dumps(merged_sol_data, sort_keys=True, indent=4))

  # with open("./package.json", "w") as fp:
  #   fp.write(json.dumps(package, sort_keys=True, indent=4))

  end = time.time()
  print(end - start)

import json, time
from merge import merge
from sol_code_extractions import extract_sol_data 
from sol_dependency_analysers import form_dependencies
# from package_generator import find_all_exported_items, generate_package


def read_sol_file(file_path):
  with open(file_path, "r") as fp:
    input = fp.read()
    fp.seek(0)
    input_lines = fp.readlines()

    return input, input_lines


if __name__ == "__main__":
  input, input_lines = read_sol_file("./ERC20.sol")

  start = time.time()

  sol_data = extract_sol_data(input, input_lines)
  dependencies = form_dependencies(sol_data)
  merged_sol_data = merge(sol_data, dependencies)
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

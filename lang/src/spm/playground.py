import json
from sol_code_extractions import extract_sol_data 
from sol_dependency_analysers import form_dependencies

input, input_lines = "", []

with open("./ERC20.sol", "r") as fp:
  input = fp.read()
  fp.seek(0)
  input_lines = fp.readlines()


if __name__ == "__main__":
  sol_data = extract_sol_data(input, input_lines)
  with open("./output.json", "w") as fp:
    fp.write(json.dumps(sol_data, sort_keys=True, indent=4))

  dependencies = form_dependencies(sol_data)
  with open("./dependencies.json", "w") as fp:
    fp.write(json.dumps(dependencies, sort_keys=True, indent=4))

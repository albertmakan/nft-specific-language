
def form_dependencies(sol_data):
  
  dependencies = {}
  for contract, contract_def in sol_data.items():
    dependencies[contract] = {
      "functions": {},
      "structs": {},
      "variables": {}
    }

    for function in contract_def["functions"]:
      function_dependencies = find_dependencies_for_function(sol_data, contract, function)
      dependencies[contract]["functions"][function] = function_dependencies

    for struct in contract_def["structs"]:
      struct_dependencies = find_dependencies_for_struct(sol_data, contract, struct)
      dependencies[contract]["structs"][struct] = struct_dependencies

    for variable in contract_def["variables"]:
      variable_dependencies = find_dependencies_for_variables(sol_data, contract, variable)
      dependencies[contract]["variables"][variable] = variable_dependencies

  return dependencies


# -------- Utility funkcije za formiranje zavisnosti i formiranje json iz nase strukture --------


def find_dependencies_for_struct(sol_data, contract, struct_name):
  struct_code = sol_data[contract]["structs"][struct_name]
  return {
    "contracts": find_dependent_contracts(sol_data, struct_code),
    "structs": find_dependent_structs(sol_data, contract, struct_code),
  }

def find_dependencies_for_function(sol_data, contract, function_name):
  function_code = sol_data[contract]["functions"][function_name]
  return {
    "contracts": find_dependent_contracts(sol_data, function_code),
    "structs": find_dependent_structs(sol_data, contract, function_code),
    "functions": find_dependent_functions(sol_data, contract, function_code),
    "variables": find_dependent_variables(sol_data, contract, function_code)
  }

def find_dependencies_for_variables(sol_data, contract, variable_name):
  variable_code = sol_data[contract]["variables"][variable_name]
  return {
    "contracts": find_dependent_contracts(sol_data, variable_code),
    "structs": find_dependent_structs(sol_data, contract, variable_code),
  }

def find_dependent_contracts(sol_data, code):
  contract_names = find_possible_contract_name(sol_data)
  dependent_contracts = []
  for contract_name in contract_names:
    if "new {0}".format(contract_name) not in code and "{0} ".format(contract_name) not in code:
      continue
    dependent_contracts.append(contract_name)
  return dependent_contracts

def find_possible_contract_name(sol_data):
  return list(sol_data.keys())


def find_dependent_structs(sol_data, contract, code):
  struct_names = find_possible_struct_names(sol_data, contract)
  dependent_structs = []
  for struct_name in struct_names:
    if "{0} ".format(struct_name) not in code and "{0}(".format(struct_name) not in code:
      continue
    dependent_structs.append(struct_name)
  return dependent_structs

def find_possible_struct_names(sol_data, contract):
  struct_names = list(sol_data[contract]["structs"].keys())
  if contract != "@global":
    struct_names.extend(sol_data["@global"]["structs"].keys())
  if sol_data[contract]["base"] is not None:
    struct_names.extend(sol_data[sol_data[contract]["base"]]["structs"].keys())
  return struct_names


def find_dependent_functions(sol_data, contract, code):
  function_names = find_possible_function_names(sol_data, contract)
  dependent_functions = []
  for function_name in function_names:
    if "{0}(".format(function_name) not in code:
      continue
    dependent_functions.append(function_name)
  return dependent_functions

def find_possible_function_names(sol_data, contract):
  function_names = list(sol_data[contract]["functions"].keys())
  if contract != "@global":
    function_names.extend(sol_data["@global"]["functions"].keys())
  if sol_data[contract]["base"] is not None:
    function_names.extend(sol_data[sol_data[contract]["base"]]["functions"].keys())

  return function_names


def find_dependent_variables(sol_data, contract, code):
  variable_names = find_possible_variable_names(sol_data, contract)
  dependent_variables = []
  for variable_name in variable_names:
    if "{0}".format(variable_name) not in code:
      continue
    dependent_variables.append(variable_name)
  return dependent_variables

def find_possible_variable_names(sol_data, contract):
  if contract == "@global":
    return []  
  
  variable_names = list(sol_data[contract]["variables"].keys())
  if sol_data[contract]["base"] is not None:
    variable_names.extend(sol_data[sol_data[contract]["base"]]["variables"].keys())

  return variable_names
import re


def form_dependencies(sol_data):
  
  dependencies = {}
  for contract, contract_def in sol_data.items():
    dependencies[contract] = {
      "functions": {},
      "structs": {},
      "variables": {},
      "events": {},
      "modifiers": {}
    }

    for function in contract_def["functions"]:
      function_dependencies = find_dependencies_for_function(sol_data, contract, function)
      if not len(function_dependencies):
        continue
      dependencies[contract]["functions"][function] = function_dependencies

    for struct in contract_def["structs"]:
      struct_dependencies = find_dependencies_for_struct(sol_data, contract, struct)
      if not len(struct_dependencies):
        continue
      dependencies[contract]["structs"][struct] = struct_dependencies

    for variable in contract_def["variables"]:
      variable_dependencies = find_dependencies_for_variables(sol_data, contract, variable)
      if not len(variable_dependencies):
        continue
      dependencies[contract]["variables"][variable] = variable_dependencies

    for event in contract_def["events"]:
      event_dependencies = find_dependencies_for_event(sol_data, contract, event)
      if not len(event_dependencies):
        continue
      dependencies[contract]["events"][event] = event_dependencies

    for modifier in contract_def["modifiers"]:
      modifier_dependencies = find_dependencies_for_modifier(sol_data, contract, modifier)
      if not len(modifier_dependencies):
        continue
      dependencies[contract]["modifiers"][modifier] = modifier_dependencies


  return dependencies


# -------- Utility funkcije za formiranje zavisnosti i formiranje json iz nase strukture --------


def sanitize_itself(name, dependencies):
  return list(filter(lambda dependency: name != dependency, dependencies))

def sanitize_empty_values(dependencies: dict):
  return {k: v for k, v in dependencies.items() if v}


def find_dependencies_for_struct(sol_data, contract, struct_name):
  struct_code = sol_data[contract]["structs"][struct_name]
  return sanitize_empty_values({
    "contracts": find_dependent_contracts(sol_data, struct_code),
    "structs": sanitize_itself(struct_name, find_dependent_structs(sol_data, contract, struct_code)),
  })

def find_dependencies_for_function(sol_data, contract, function_name):
  function_code = sol_data[contract]["functions"][function_name]
  return sanitize_empty_values({
    "contracts": find_dependent_contracts(sol_data, function_code),
    "structs": find_dependent_structs(sol_data, contract, function_code),
    "functions": sanitize_itself(function_name, find_dependent_functions(sol_data, contract, function_code)),
    "variables": find_dependent_variables(sol_data, contract, function_code),
    "events": find_dependent_events(sol_data, contract, function_code),
    "modifiers": find_dependent_modifiers(sol_data, contract, function_code)
  })

def find_dependencies_for_variables(sol_data, contract, variable_name):
  variable_code = sol_data[contract]["variables"][variable_name]
  return sanitize_empty_values({
    "contracts": find_dependent_contracts(sol_data, variable_code),
    "structs": find_dependent_structs(sol_data, contract, variable_code),
  })

def find_dependencies_for_event(sol_data, contract, event_name):
  event_code = sol_data[contract]["events"][event_name]
  return sanitize_empty_values({
    "contracts": find_dependent_contracts(sol_data, event_code),
    "structs": find_dependent_structs(sol_data, contract, event_code),
  })

def find_dependencies_for_modifier(sol_data, contract, modifier_name):
  modifier_code = sol_data[contract]["modifiers"][modifier_name]
  return sanitize_empty_values({
    "contracts": find_dependent_contracts(sol_data, modifier_code),
    "structs": find_dependent_structs(sol_data, contract, modifier_code),
    "functions": sanitize_itself(modifier_name, find_dependent_functions(sol_data, contract, modifier_code)),
    "variables": find_dependent_variables(sol_data, contract, modifier_code),
    "events": find_dependent_events(sol_data, contract, modifier_code)
  })

def find_dependent_contracts(sol_data, code):
  contract_names = find_possible_contract_name(sol_data)
  return [name for name in contract_names if re.search(fr"\b{name}\b", remove_string_literals(code))]

def find_possible_contract_name(sol_data):
  return list(sol_data.keys())


def find_dependent_structs(sol_data, contract, code):
  struct_names = find_possible_struct_names(sol_data, contract)
  return [name for name in struct_names if re.search(fr"\b{name}\b", remove_string_literals(code))]

def find_possible_struct_names(sol_data, contract):
  struct_names = list(sol_data[contract]["structs"].keys())
  if contract != "@global":
    struct_names.extend(sol_data["@global"]["structs"].keys())

  contracts_chain = find_contract_chain(contract, sol_data)
  for contract in contracts_chain:
    struct_names.extend(sol_data[sol_data[contract]["base"]]["structs"].keys())

  return struct_names


def find_dependent_functions(sol_data, contract, code):
  function_names = find_possible_function_names(sol_data, contract)
  return [name for name in function_names if re.search(fr"\b{name}\b", remove_string_literals(code))]


def find_possible_function_names(sol_data, contract):
  function_names = list(sol_data[contract]["functions"].keys())
  if contract != "@global":
    function_names.extend(sol_data["@global"]["functions"].keys())

  contracts_chain = find_contract_chain(contract, sol_data)
  for contract in contracts_chain:
    function_names.extend(sol_data[sol_data[contract]["base"]]["functions"].keys())

  return function_names


def find_dependent_variables(sol_data, contract, code):
  variable_names = find_possible_variable_names(sol_data, contract)
  return [name for name in variable_names if re.search(fr"\b{name}\b", remove_string_literals(code))]

def find_possible_variable_names(sol_data, contract):
  if contract == "@global":
    return []  
  
  variable_names = list(sol_data[contract]["variables"].keys())

  contracts_chain = find_contract_chain(contract, sol_data)
  for contract in contracts_chain:
    variable_names.extend(sol_data[sol_data[contract]["base"]]["variables"].keys())

  return variable_names


def find_dependent_events(sol_data, contract, code):
  event_names = find_possible_event_names(sol_data, contract)
  return [name for name in event_names if re.search(fr"\bemit\s+{name}\b", remove_string_literals(code))]

def find_possible_event_names(sol_data, contract):
  event_names = list(sol_data[contract]["events"].keys())

  contracts_chain = find_contract_chain(contract, sol_data)
  for contract in contracts_chain:
    event_names.extend(sol_data[sol_data[contract]["base"]]["events"].keys())

  return event_names


def find_dependent_modifiers(sol_data, contract, code):
  modifier_names = find_possible_modifier_names(sol_data, contract)
  return [name for name in modifier_names if re.search(fr"\b{name}\b", remove_string_literals(code))]

def find_possible_modifier_names(sol_data, contract):
  modifier_names = list(sol_data[contract]["modifiers"].keys())

  contracts_chain = find_contract_chain(contract, sol_data)
  for contract in contracts_chain:
    modifier_names.extend(sol_data[sol_data[contract]["base"]]["modifiers"].keys())

  return modifier_names


def find_contract_chain(contract, sol_data):
  contracts = []
  current_contract = contract
  while sol_data[current_contract]["base"]:
    contracts.append(current_contract)
    current_contract = sol_data[current_contract]["base"]
  return contracts


def remove_string_literals(text: str):
  string_rexeg = re.compile(r"\"(([^\"]|\\\")*[^\\])?\"")
  return re.sub(string_rexeg, "", text)

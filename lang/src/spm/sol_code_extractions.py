import re
from solidity_parser import parser

def extract_sol_data(input, input_lines):

  contracts = extract_sol_contracts(input)
  sourceUnit = parser.parse(input.replace('{{', '"{').replace('}}', '}"'), loc=True)

  global_code = input
  for contract_code in contracts.values(): global_code = global_code.replace(contract_code, "")
  contracts["@global"] = global_code

  for contract, code in contracts.items():
    state_variables = {}
    base = None
    for child in sourceUnit.children:
      if child["type"] == "ContractDefinition" and child["name"] == contract:
        state_variables = extract_state_variables(child, input_lines)
        base = extract_base_contract(child)

    contracts[contract] = {
      "base": base,
      "code": code,
      "functions": extract_sol_functions(code),
      "modifiers": extract_sol_modifiers(code),
      "structs": extract_sol_structs(code),
      "events": extract_sol_events(code),
      "variables": state_variables,
    }

    if contract == '@global':
      contracts[contract]["imports"] = extract_imports(sourceUnit)

  return contracts


# -------- Utility funkcije za extrakciju koda i formiranje json iz solidity koda --------
def eat_word(text):
  chars = []
  for char in text:
    if char in [' ', '(', '{']:
      return "".join(chars)

    chars.append(char)

def extract_sol_contracts(code):
  contract_start_positions = [match.start(0) for match in re.finditer(r"contract .*(is|\{)", code)]
  contracts = extract_chucks(code, contract_start_positions)

  return { eat_word(contract.replace("contract ", "")): contract for contract in contracts }

def extract_sol_functions(code):
  function_start_positions = [match.start(0) for match in re.finditer(r"function .*\(", code)]
  functions = extract_chucks(code, function_start_positions)

  return { eat_word(function.replace("function ", "")): function for function in functions }

def extract_sol_modifiers(code):
  modifiers_start_positions = [match.start(0) for match in re.finditer(r"modifier .*", code)]
  modifiers = extract_chucks(code, modifiers_start_positions)

  return { eat_word(modifier.replace("modifier ", "")): modifier for modifier in modifiers }

def extract_sol_structs(code):
  struct_start_positions = [match.start(0) for match in re.finditer(r"struct .*\{", code)]
  structs = extract_chucks(code, struct_start_positions)

  return { eat_word(struct.replace("struct ", "")): struct for struct in structs }

def extract_sol_events(code):
  event_start_positions = [match.start(0) for match in re.finditer(r"event .*\(", code)]
  events = extract_till_char(code, event_start_positions, ';')

  return { eat_word(event.replace("event ", "")): event for event in events }

def extract_chucks(code, positions):
  chunks = []
  for start_position in positions:
    bracket_counter = 0
    chuck_chars = []
    for char in code[start_position:-1]:
      chuck_chars.append(char)
      if char == '{':
        bracket_counter += 1

      if char == '}':
        if bracket_counter == 1:
          break

        bracket_counter -= 1

    chunks.append("".join(chuck_chars))

  return chunks

def extract_till_char(code, positions, last_char):
  chunks = []
  for start_position in positions:
    chuck_chars = []
    for char in code[start_position:-1]:
      chuck_chars.append(char)
      if char == last_char:
        break

    chunks.append("".join(chuck_chars))

  return chunks
    
def extract_state_variables(contractAST, code_lines):
  state_variables = {}
  for subNode in contractAST["subNodes"]:
    if subNode["type"] != "StateVariableDeclaration":
      continue

    state_variable_name = subNode["variables"][0]["name"]
    state_variable_code = extract_text_using_pos(code_lines, subNode["loc"]["start"], subNode["loc"]["end"])

    state_variables[state_variable_name] = state_variable_code

  return state_variables

def extract_text_using_pos(lines, start, end):
    start_line, start_pos = start["line"], start["column"]
    end_line, end_pos = end["line"], end["column"]

    if start_line == end_line:
      return lines[start_line-1][start_pos:end_pos+1]

    definition = ""
    for line in range(start_line, end_line+1):
      if line == start_line:
        definition += lines[line-1][start_pos:]
        continue
      
      if line == end_line:
        definition += lines[line-1][0:end_pos+1]
        continue

      definition += lines[line-1]
    return definition

def extract_base_contract(contractAST):
  if "baseContracts" not in contractAST or len(contractAST["baseContracts"]) == 0:
    return None
  
  return contractAST["baseContracts"][0]["baseName"]["namePath"]

def extract_imports(ast):
  imports = []
  for node in ast["children"]:
    if node["type"] != "ImportDirective":
      continue

    imports.append('"{0}"'.format(node["path"]))

  return imports
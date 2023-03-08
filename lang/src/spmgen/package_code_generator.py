
def generate_package_code(sol_data, exported_items):
  package = {}
  for exported_item in exported_items:
    contract, sol_item, sol_type = exported_item.split('_')
    contract_chain = _find_contract_chain_upwards(contract, sol_data)
    for contract_in_chain in contract_chain:
      if contract_in_chain not in package:
        package[contract_in_chain] = {
          "base": sol_data[contract_in_chain]["base"],
          "code": sol_data[contract_in_chain]["code"]
        }

    if sol_type not in package[contract]:
      package[contract][sol_type] = { }
    package[contract][sol_type][sol_item] = sol_data[contract][sol_type][sol_item]

  return package


def find_all_exported_items(sol_data, exports):
  queue = [_compute_initial_queue_item(sol_data, export) for export in exports]
  exported_items = []

  while len(queue):
    possible_contracts, item_name, item_type = queue.pop()

    if item_type == 'contracts':
      queue.extend(_form_queue_items_for_dependent_contract(sol_data, [item_name]))
    else:
      for contract in possible_contracts:
        if item_type not in sol_data[contract] or item_name not in sol_data[contract][item_type]:
          continue

        key = "{0}_{1}_{2}".format(contract, item_name, item_type)
        if key not in exported_items:
          exported_items.append(key)

        if not "dependencies" in sol_data[contract][item_type][item_name]:
          continue

        for dependency_sol_type, dependency_sol_items in sol_data[contract][item_type][item_name]["dependencies"].items():
          if dependency_sol_type == "contracts":
            queue.extend(_form_queue_items_for_dependent_contract(sol_data, dependency_sol_items))
          else:
            queue.extend(_form_queue_items_for_dependency_other_then_contract(sol_data, contract, dependency_sol_type, dependency_sol_items))
        
        break

  return exported_items

def _compute_initial_queue_item(sol_data, export):
  export_tokens = export.split('.')

  if export_tokens[-1] == 'contracts':
    return [[export_tokens[0]], export_tokens[0], export_tokens[1]]

  return [_find_contract_chain_downwards(export_tokens[0], sol_data), export_tokens[1], export_tokens[2]]


def _form_queue_items_for_dependent_contract(sol_data, dependent_contracts):
  queue_items = []
  for dependent_contract in dependent_contracts:
    for contract_in_chain in _find_contract_chain_downwards(dependent_contract, sol_data, False):
      for sol_type, sol_items in sol_data[contract_in_chain].items():
        if sol_type in ["base", "code"]:
          continue

        queue_items.extend([[[contract_in_chain, '@global'], sol_item, sol_type] for sol_item in sol_items])
  
  return queue_items

def _form_queue_items_for_dependency_other_then_contract(sol_data, contract, dependency_sol_type, dependency_sol_items):
  dependency_possible_contracts = _find_contract_chain_downwards(contract, sol_data)
  
  return [[dependency_possible_contracts, dependency_name, dependency_sol_type] for dependency_name in dependency_sol_items]


def _find_contract_chain_downwards(contract, sol_data, add_global = True):
  contracts = []
  current_contract = contract
  while current_contract is not None:
    contracts.append(current_contract)
    current_contract = sol_data[current_contract]['base']

  if contract != '@global' and add_global:
    contracts.append('@global')

  return contracts

def _find_contract_chain_upwards(contract, sol_data):
  contracts = []
  current_contract = contract
  while current_contract is not None:
    contracts.append(current_contract)
    new_contract = None
    for contract in sol_data:
      if sol_data[contract]['base'] == current_contract:
        new_contract = contract
    current_contract = new_contract

  return contracts
  
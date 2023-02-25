
def generate_package(sol_data, exported_items):
  package = {}
  for exported_item in exported_items:
    contract, sol_item, sol_type = exported_item.split('_')
    if contract not in package:
      package[contract] = {
        "base": sol_data[contract]["base"],
        "code": sol_data[contract]["code"]
      }
    if sol_type not in package[contract]:
      package[contract][sol_type] = { }
    package[contract][sol_type][sol_item] = sol_data[contract][sol_type][sol_item]

  return package

def find_all_exported_items(sol_data, functions):
  queue = [[[function.split('.')[0], '@global'], function.split('.')[1], 'functions'] for function in functions]
  exported_items = []

  while len(queue):
    possible_contracts, item_name, item_type = queue.pop()

    for contract in possible_contracts:
      if not item_name in sol_data[contract][item_type]:
        continue

      key = "{0}_{1}_{2}".format(contract, item_name, item_type)
      if key not in exported_items:
        exported_items.append(key)

      if not "dependencies" in sol_data[contract][item_type][item_name]:
        continue

      for dependency_sol_type, dependency_sol_items in sol_data[contract][item_type][item_name]["dependencies"].items():
        if dependency_sol_type == "contracts":
          queue.extend(form_queue_items_for_dependent_contract(sol_data, dependency_sol_items))
        else:
          queue.extend(form_queue_items_for_dependency_other_then_contract(contract, dependency_sol_type, dependency_sol_items))
      
      break

  return exported_items


def form_queue_items_for_dependent_contract(sol_data, dependent_contracts):
  for dependent_contract in dependent_contracts:
    for sol_type, sol_items in sol_data[dependent_contract].items():
      if sol_type in ["base", "code"]:
        continue

      return [[[dependent_contract, '@global'], sol_item, sol_type] for sol_item in sol_items]


def form_queue_items_for_dependency_other_then_contract(contract, dependency_sol_type, dependency_sol_items):
  dependency_possible_contracts = [contract, '@global'] if contract != '@global' else [contract]
  
  return [[dependency_possible_contracts, dependency_name, dependency_sol_type] for dependency_name in dependency_sol_items]

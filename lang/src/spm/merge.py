import jsonmerge

def adapt_sol_data_for_merge(sol_data):
    adapted_sol_data = {}
    for contract, contract_data in sol_data.items():
        adapted_sol_data[contract] = {
            "base": contract_data["base"],
            "code": contract_data["code"],
            "functions": { key: { "code": value } for key, value in contract_data["functions"].items() },
            "structs": { key: { "code": value } for key, value in contract_data["structs"].items() },
            "variables": { key: { "code": value } for key, value in contract_data["variables"].items() },
            "events": { key: { "code": value } for key, value in contract_data["events"].items() },
            "modifiers": { key: { "code": value } for key, value in contract_data["modifiers"].items() },
        }
    
    return adapted_sol_data

def adapt_dependencies_for_merge(dependencies):
    adapted_dependencies = {}
    for contract, contract_data in dependencies.items():
        adapted_dependencies[contract] = {
            "structs": {},
            "functions": {},
            "variables": {},
            "events": {},
            "modifiers": {}
        }

        for sol_type, sol_type_data in contract_data.items():
            for sol_type_instance, sol_type_instance_dependencies in sol_type_data.items():
                adapted_dependencies[contract][sol_type][sol_type_instance] = {
                    "dependencies": sol_type_instance_dependencies
                }
    
    return adapted_dependencies
    
def merge_data_with_dependencies(sol_data, dependencies):
    adapted_sol_data = adapt_sol_data_for_merge(sol_data)
    adapted_dependencies = adapt_dependencies_for_merge(dependencies)

    return jsonmerge.merge(adapted_sol_data, adapted_dependencies)
    
def merge_data(sol_data1, sol_data2):
    return jsonmerge.merge(sol_data1, sol_data2)
    

import json
from spl import Script


package_cache = {}


def generate(model: Script, output_file: str):
    contracts = {
        c.name: {
            'f': {
                f.name: {
                    'code': find_data(f.name),
                    'params': {p.name: str(p.value) for p in f.params.parameters},
                    'mod': []
                } for f in c.implementation.methods},
            'v': {},
            'm': {}
        } for c in model.contract.contracts
    }

    manager = model.administration.main_administrator
    for ca in manager.contract_administrators:
        for method in ca.methods:
            contracts[ca.contract.name]['f'][method.name]['mod'].append(manager.package)

    for admin in model.administration.extension_administrators:
        for ca in admin.contract_administrators:
            for method in ca.methods:
                contracts[ca.contract.name]['f'][method.name]['mod'].append(admin.package)

    with open(output_file, 'w') as f:
        json.dump(contracts, f, indent=4)


def find_data(func_path: str):
    pack_name, *path, func_name = func_path.split('.')
    package = None
    if not pack_name in package_cache:
        with open(f'{pack_name}.json') as pack:
            package = json.load(pack)
        package_cache[pack_name] = package
    else:
        package = package_cache[pack_name]

    current = package
    for key in path:
        if key in current:
            current = current[key]
        else:
            return None
    return current['functions'][func_name]
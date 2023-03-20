from dataclasses import dataclass
from datetime import datetime
import json
from typing import Dict, List, Set, Tuple
import re
from jinja2 import BaseLoader, Environment

from spl.model import Script, AddressSet, Percentage, Address
from .constants import *

package_cache = {}
packages_v: Dict[str,str] = None

template = """/* Generated by SPL [{{timestamp}}] */
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

// =========== DEPENDENCIES ===========
{% for dep in dependencies | sort_deps %}
{{dep.code}}
{% endfor %}
// ========== YOUR CONTRACTS ==========
{% for contract in contracts %}
contract {{contract.name}} {
    {% for dep in contract.dependencies | sort_deps %}
    {{dep.code}}
    {% endfor %}
    {% for func in contract.functions.values() %}
    {{func.code}}
    {% endfor %}
}
{% endfor %}
"""


def generate(model: Script, output_file: str):
    dependencies: Set[Dependency] = set()
    manager = model.administration.main_administrator
    contracts = {
        c.name: Contract(
            name=c.name,
            functions={
                **{
                    f.name: Function(
                        name=f.name,
                        params={p.name: format_param(p.literal)
                                for p in f.params.parameters},
                        modifiers=set()
                    ) for f in c.implementation.methods
                },
                **{
                    admin.method.name: Function(
                        name=admin.method.name,
                        params={p.name: format_param(p.literal)
                                for p in admin.method.params.parameters},
                        is_modifier=True,
                        modifiers=set()
                    ) for admin in model.administration.extension_administrators
                },
                manager.method.name: Function(
                    name=manager.method.name,
                    params={p.name: format_param(p.literal)
                            for p in manager.method.params.parameters},
                    is_modifier=True,
                    modifiers=set()
                )
            },
            dependencies=set(),
        ).resolve_code_and_dependencies(dependencies)
        .insert_params() for c in model.contract_section.contracts
    }

    for ca in manager.contract_administrators:
        for method in ca.methods:
            contracts[ca.contract.name].functions[method.name].modifiers.add(
                manager.method.name)

    for admin in model.administration.extension_administrators:
        for ca in admin.contract_administrators:
            for method in ca.methods:
                contracts[ca.contract.name].functions[method.name].modifiers.add(
                    admin.method.name)

    for contract in contracts.values():
        contract.remove_redundant_dependencies()
        contract.insert_modifiers()

    env = Environment(loader=BaseLoader)
    env.filters["sort_deps"] = lambda deps: sorted(list(deps), key=lambda d: (d.type, d.priority), reverse=True)
    env.from_string(template).stream(
        dependencies=dependencies,
        contracts=contracts.values(),
        timestamp=datetime.now()
    ).dump(output_file)


@dataclass
class Dependency:
    name: str
    code: str
    type: str
    priority: int = 0

    def __eq__(self, other):
        if not isinstance(other, Dependency):
            return False
        return self.name == other.name and self.code == other.code and self.type == other.type

    def __hash__(self):
        return hash((self.name, self.code, self.type))


@dataclass
class Function:
    params: Dict[str, str]
    name: str
    modifiers: Set[str]
    code: str = ""
    is_modifier: bool = False
    name_in_code: str = ""

    def insert_params(self):
        for par in self.params:
            matches: List[str] = re.findall(
                fr'{{{{\s*{par}\s*:\s*\w+\s*}}}}', self.code)
            if not matches:
                continue
            par_type = matches[0][2:-2].split(':')[1].strip()
            self.code = self.code.replace(matches[0], self.params[par])
        left: List[str] = re.findall(
            fr'{{{{\s*\w+\s*:\s*\w+\s*}}}}', self.code)
        if left:
            raise Exception("Missing params:", left)
        return self


@dataclass
class Contract:
    functions: Dict[str, Function]
    dependencies: Set[Dependency]
    name: str

    def resolve_code_and_dependencies(self, globals: Set[Dependency]):
        load_package_json()
        for fun in self.functions.values():
            try:
                self._resolve(fun, globals)
            except KeyError:
                raise Exception(
                    f"{'Modifier' if fun.is_modifier else 'Function'} '{fun.name}' not found")
        return self

    def insert_params(self):
        for fun in self.functions.values():
            fun.insert_params()
        return self

    def _resolve(self, fun: Function, globals: Set[Dependency]):
        pack_name, p, t = get_packname_path_and_type(fun.name)

        *path, func_name = p.split('.')

        snippets = package_cache[pack_name][SOL_CODE]

        current_block, parent_block = snippets, None
        for key in path:
            parent_block = current_block
            current_block = current_block[key]

        result = t in current_block and current_block[t].get(func_name)
        base_names = current_block[BASE]
        chain = find_contract_chain(path[-1], parent_block, base_names)
        curr_name = path[-1]
        for base_name in chain:
            if result: break
            current_block = parent_block[base_name]
            curr_name = base_name
            result = t in current_block and current_block[t].get(func_name)

        fun.code = result[CODE]
        fun.name_in_code = func_name

        def find_dep(thing: dict):
            if DEPENDENCIES not in thing:
                return
            dependencies: Dict[str, List[str]] = thing[DEPENDENCIES]
            for dep_type in dependencies:
                for name in dependencies[dep_type]:
                    if dep_type == CONTRACTS:
                        c = parent_block[name]
                        globals.add(Dependency(name, c[CODE], dep_type))
                        find_contract_dependencies(parent_block, name, globals)
                        continue

                    dep = dep_type in current_block and current_block[dep_type].get(name)
                    if dep:
                        self.dependencies.add(Dependency(name, dep[CODE], dep_type))
                        find_dep(dep)
                        continue

                    base_names = current_block[BASE]
                    chain = find_contract_chain(curr_name, parent_block, base_names)
                    for base_name in chain:
                        base = parent_block[base_name]
                        dep = dep_type in base and base[dep_type].get(name)
                        if dep: break

                    if dep:
                        self.dependencies.add(Dependency(name, dep[CODE], dep_type))
                        find_dep(dep)
                        continue
                    dep = parent_block[GLOBAL][dep_type][name]
                    globals.add(Dependency(name, dep[CODE], dep_type))
                    find_dep(dep)

        find_dep(result)

    def insert_modifiers(self):
        for fun in self.functions.values():
            if not fun.modifiers:
                continue
            to_insert = " ".join((self.functions[m].name_in_code for m in fun.modifiers))
            block_start = fun.code.find('{')
            returns_loc = fun.code.find('returns', 0, block_start)
            idx = returns_loc if returns_loc != -1 else block_start
            fun.code = fun.code[:idx] + to_insert + fun.code[idx-1:]

    def remove_redundant_dependencies(self):
        for fun in self.functions.values():
            d = Dependency(fun.name_in_code, fun.code, MODIFIERS if fun.is_modifier else FUNCTIONS)
            if d in self.dependencies:
                self.dependencies.remove(d)



def format_param(param):
    if isinstance(param, Address):
        return f"address({param.value})"
    if isinstance(param, AddressSet):
        return f'[{", ".join((f"address({a.value})" for a in param.values))}]'
    if isinstance(param, Percentage):
        return str(param.percent)
    if isinstance(param, str):
        param = param.replace('"', "'")
        return f'{"" if param.isascii() else "unicode"}"{param}"'
    return str(param)


def find_contract_dependencies(_package: dict, c_name: str, globals: Set[Dependency], p=0):
    contract = _package[c_name]
    p += 1
    base_names = contract[BASE]
    for base_name in base_names:
        globals.add(Dependency(base_name, _package[base_name][CODE], CONTRACTS, p))
        find_contract_dependencies(_package, base_name, globals, p)
    for thing_type in contract:
        if thing_type == CODE or thing_type == BASE:
            continue
        things = contract[thing_type]
        for thing_name in things:
            thing = things[thing_name]
            if DEPENDENCIES not in thing:
                continue
            dependencies: Dict[str, List[str]] = thing[DEPENDENCIES]
            for dep_type in dependencies:
                for name in dependencies[dep_type]:
                    if dep_type == CONTRACTS:
                        c = _package[name]
                        globals.add(Dependency(name, c[CODE], dep_type, p))
                        find_contract_dependencies(_package, name, globals, p)
                        continue
                    if name in contract[dep_type] or any((name in _package[base_name][dep_type] for base_name in base_names)):
                        continue
                    dep = _package[GLOBAL][dep_type][name]
                    globals.add(Dependency(name, dep[CODE], dep_type, p))


def load_package_json():
    global packages_v
    if not packages_v:
        with open(PACKAGE_JSON_PATH) as pack:
            packages_v = json.load(pack)[PACKAGES]


def get_packname_path_and_type(fqn: str) -> Tuple[str,str,str]:
    pack_name, *path = fqn.split('.')

    if not pack_name in package_cache:
        v = packages_v[pack_name]
        with open(f'{SPM_PACKAGES_PATH}/{pack_name}_{v}.json') as pack:
            package_cache[pack_name] = json.load(pack)
    package = package_cache[pack_name][DEFINITION][pack_name]

    current_block = package
    for key in path:
        current_block = current_block[key]
    
    if not ('type' in current_block and 'path' in current_block):
        raise Exception(f"{fqn} not found.")
    
    return pack_name, current_block['path'], current_block['type']


def find_contract_chain(contract_name: str, sol_data: dict, chain: list=None):
    contracts = chain or []
    bases = sol_data[contract_name][BASE]
    contracts.extend(bases)
    for bc in bases:
        find_contract_chain(bc, sol_data, contracts)
    return contracts


# TODO:
# handle name conflict
# contract dependencies
# insert modifiers params?
# param type check?
# difference between managed and extended?

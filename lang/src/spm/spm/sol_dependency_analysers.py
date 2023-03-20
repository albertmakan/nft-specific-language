import re

from .constants import *


def form_dependencies(sol_data: dict):
    for contract_name, contract_def in sol_data.items():
        if contract_name == GLOBAL:
            continue
        for type in contract_def:
            if type == BASE or type == CODE:
                continue
            for name in contract_def[type]:
                find_dependencies_for_thing(type, sol_data, contract_name, name)
    return sol_data


def find_dependencies_for_thing(type: str, sol_data: dict, contract_name: str, name: str):
    dependent_types = [CONTRACTS, STRUCTS]
    if type == FUNCTIONS or type == MODIFIERS:
        dependent_types.extend([FUNCTIONS, VARIABLES, EVENTS])
    if type == MODIFIERS:
        dependent_types.extend([MODIFIERS])
    thing = sol_data[contract_name][type][name]
    dependencies = {t: find_dependent_names(t, sol_data, contract_name, thing[CODE], name) for t in dependent_types}
    dependencies = {k: v for k, v in dependencies.items() if v}
    if dependencies:
        thing[DEPENDENCIES] = dependencies


def find_possible_names(type: str, sol_data: dict, contract_name: str):
    names = []
    if type in sol_data[GLOBAL]:
        names.extend(sol_data[GLOBAL][type].keys())
    if contract_name == GLOBAL:
        return names
    names.extend(sol_data[contract_name][type].keys())
    for contract_name in find_contract_chain(contract_name, sol_data):
        names.extend(sol_data[contract_name][type].keys())
    return names


def find_dependent_names(type: str, sol_data: dict, contract_name: str, code: str, this_name: str):
    names = list(sol_data.keys()) if type == CONTRACTS else find_possible_names(type, sol_data, contract_name)
    code_wo_str = remove_string_literals(code)
    return [name for name in names if name != this_name and re.search(fr"\b{name}\b", code_wo_str)]


def find_contract_chain(contract_name: str, sol_data: dict, chain: list=None):
    contracts = chain or []
    bases = sol_data[contract_name][BASE]
    contracts.extend(bases)
    for bc in bases:
        find_contract_chain(bc, sol_data, contracts)
    return contracts


def remove_string_literals(text: str):
    string_rexeg = re.compile(r"\"(([^\"]|\\\")*[^\\])?\"")
    return re.sub(string_rexeg, "", text)

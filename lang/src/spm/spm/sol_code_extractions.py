from solidity_parser import parser
from .constants import *


def extract_sol_data(sol_code: str):
    source_unit = parser.parse(sol_code.replace('{{', '"{').replace('}}', '}"'), loc=True)
    source_object = parser.objectify(source_unit)

    contracts = {
        name: {
            BASE: [bc.baseName.namePath for bc in contract._node.baseContracts],
            **extract_code(sol_code, contract._node.loc),
            FUNCTIONS: {k: extract_code(sol_code, v._node.loc) for k, v in contract.functions.items()},
            MODIFIERS: {k: extract_code(sol_code, v._node.loc) for k, v in contract.modifiers.items()},
            STRUCTS: {k: extract_code(sol_code, v.loc) for k, v in contract.structs.items()},
            EVENTS: {k: extract_code(sol_code, v._node.loc) for k, v in contract.events.items()},
            VARIABLES: {k: extract_code(sol_code, v.loc) for k, v in contract.stateVars.items()},
        } for name, contract in source_object.contracts.items()
    }
    contracts[GLOBAL] = {
        FUNCTIONS: {s.name: extract_code(sol_code, s.loc) for s in source_object._node.children if s.type == 'FunctionDefinition'},
        STRUCTS: {s.name: extract_code(sol_code, s.loc) for s in source_object._node.children if s.type == 'StructDefinition'},
        IMPORTS: [i.path for i in source_object.imports],
        BASE: [], CODE: ''
    }
    return {k: v for k, v in contracts.items() if not CODE in v or not v[CODE].startswith("interface")}


def find_pos(string: str, line: str, col: int):
    i = string.find('\n')
    n = 0
    while i >= 0 and n < line-2:
        i = string.find('\n', i + 1)
        n += 1
    return i + 1 + col if i >= 0 else -1


def extract_code(sol_code: str, loc):
    sp = find_pos(sol_code, loc['start']['line'], loc['start']['column'])
    ep = find_pos(sol_code, loc['end']['line'], loc['end']['column'])
    return {CODE: sol_code[sp:ep+1]}

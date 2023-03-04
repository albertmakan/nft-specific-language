from dataclasses import dataclass
import json
from typing import Any, Dict, List, Set, Tuple
from spl import Script, AddressSet, Percentage
import re

dep_set_type = Set[Tuple[str, str, str]]

package_cache = {}


def generate(model: Script, output_file: str):
    dependencies: dep_set_type = set()
    contracts = {
        c.name: Contract(
            name=c.name,
            functions={
                f.name: Function(
                    name=f.name,
                    code="",
                    params={p.name: format_param(p.value)
                            for p in f.params.parameters},
                    mod=[]
                ) for f in c.implementation.methods
            },
            dependencies=set(),
        ).resolve_code_and_dependencies(dependencies)
        .insert_params() for c in model.contract.contracts
    }

    manager = model.administration.main_administrator
    for ca in manager.contract_administrators:
        for method in ca.methods:
            contracts[ca.contract.name].functions[method.name].mod.append(
                manager.package)

    for admin in model.administration.extension_administrators:
        for ca in admin.contract_administrators:
            for method in ca.methods:
                contracts[ca.contract.name].functions[method.name].mod.append(
                    admin.package)

    with open(output_file, 'w') as f:
        f.write("// SPDX-License-Identifier: MIT\npragma solidity ^0.8.17;\n\n")
        f.write("//"+"DEPENDENCIES".center(100, '=')+'\n\n')
        for d in sorted(list(dependencies), key=lambda d: d[2], reverse=True):
            f.write(d[1]+'\n')
        f.write("//"+"YOUR CONTRACTS".center(100, '=')+'\n\n')
        for c in contracts.values():
            f.write(f"\ncontract {c.name} {{\n")
            for d in sorted(list(c.dependencies), key=lambda d: d[2], reverse=True):
                f.write('\t'+d[1]+'\n')
            for m in c.functions.values():
                f.write('\t'+m.code+'\n')
            f.write("\n}")


@dataclass
class Function:
    code: str
    params: Dict[str, Any]
    mod: list
    name: str

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


@dataclass
class Contract:
    functions: Dict[str, Function]
    dependencies: dep_set_type
    name: str

    def resolve_code_and_dependencies(self, globals: dep_set_type):
        for fun in self.functions.values():
            try:
                self._resolve(fun, globals)
            except KeyError:
                raise Exception(f"Function '{fun.name}' not found")
        return self

    def insert_params(self):
        for fun in self.functions.values():
            fun.insert_params()
        return self

    def _resolve(self, fun: Function, globals: dep_set_type):
        pack_name, *path, func_name = fun.name.split('.')

        if not pack_name in package_cache:
            with open(f'{pack_name}.json') as pack:
                package_cache[pack_name] = json.load(pack)
        package = package_cache[pack_name]

        current, parent = package, None
        for key in path:
            parent = current
            current = current[key]
        result = current['functions'][func_name]
        fun.code = result['code']

        def find_dep(_c: dict, _p: dict, thing: dict):
            if 'dependencies' not in thing:
                return
            dependencies: Dict[str, List[str]] = thing['dependencies']
            for dep_type in dependencies:
                for name in dependencies[dep_type]:
                    if dep_type == 'contracts':
                        c = _p[name]
                        globals.add((name, c["code"], dep_type))
                        # TODO dependencies
                        continue

                    dep = _c[dep_type].get(name, None)
                    if dep:
                        self.dependencies.add((name, dep["code"], dep_type))
                        find_dep(_c, _p, dep)
                        continue
                    base = _c['base']
                    if base:
                        dep = _p[base][dep_type].get(name, None)
                        if dep:
                            self.dependencies.add(
                                (name, dep["code"], dep_type))
                            find_dep(_c, _p, dep)
                        continue
                    dep = _p["@global"][dep_type].get(name, None)
                    globals.add((name, dep["code"], dep_type))
                    find_dep(_c, _p, dep)

        find_dep(current, parent, result)


def format_param(param):
    if isinstance(param, AddressSet):
        return f'[{", ".join((f"address({a})" for a in param.values))}]'
    if isinstance(param, Percentage):
        return str(param.percent)
    if isinstance(param, str):
        return f'"{param}"'
    return str(param)

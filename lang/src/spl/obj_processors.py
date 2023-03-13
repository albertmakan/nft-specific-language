from model import Construct, ContractAdministrator, ContractDefinition, Method, PackageSection, Parameters, Percentage, Script


def _find_package_section(construct: Construct):
    c: Construct = construct.parent
    while not isinstance(c, Script):
        c = c.parent
    return c.package_section


def package_processor(package_section: PackageSection):
    names = []
    for pack in package_section.packages:
        if not pack.alias:
            pack.alias = pack.id.split('.')[-1]
        if pack.alias in names:
            raise Exception(f"Multiple imports with same name: '{pack.alias}'")
        names.append(pack.alias)


def method_processor(method: Method):
    p = method.name.split('.')
    package_section = _find_package_section(method)
    if not package_section:
        raise Exception("No package section")
    pack = next((x for x in package_section.packages if x.alias == p[0]), None)
    if not pack:
        raise Exception(f"Package '{p[0]}' not found")
    method.name = pack.id + (('.' + p[-1]) if len(p)>1 else '')
    if not method.params:
        method.params = Parameters(method, [])


def contract_admin_processor(contract_admin: ContractAdministrator):
    methods = []
    for m in contract_admin.methods:
        method = next((x for x in contract_admin.contract.implementation.methods if x.name == m.name), None)
        if not method:
            raise Exception(f"Method '{m.name}' not found in {contract_admin.contract.name}")
        methods.append(method)
    contract_admin.methods = methods


def percent_processor(percentage: Percentage):
    percentage.percent = int(percentage.percent)


def contract_processor(contract: ContractDefinition):
    methods = []
    for m in contract.implementation.methods:
        if m.name in methods:
            raise Exception(f"Duplicate method in {contract.name}: '{m.name}'")
        methods.append(m.name)
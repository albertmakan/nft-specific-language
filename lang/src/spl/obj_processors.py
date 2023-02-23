from model import Construct, Method, PackageSection, Script


def _find_package_section(construct: Construct):
    c: Construct = construct.parent
    while not isinstance(c, Script):
        c = c.parent
    return c.package


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

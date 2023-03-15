

def load_local_packages():
    global local_packages
    if local_packages is not None:
        return
    package_json_path = os.path.join(
        spm_server.workspace.root_path, "package.json")
    with open(package_json_path, "r") as fp:
        package_json = json.loads(fp.read())
        if "packages" in package_json:
            local_packages = package_json["packages"]


def get_package_definition(package_name):

    if package_name in package_definitions:
        return package_definitions[package_name]

    if not package_name in local_packages:
        return None

    package_version = local_packages[package_name]

    package_path = os.path.join(spm_server.workspace.root_path,
                                "spm_packages", f"{package_name}_{package_version}.json")
    with open(package_path, "r") as fp:
        package = json.loads(fp.read())
        if "definition" in package:
            package_definition = package["definition"]
            package_definitions[package_name] = package_definition

            return package_definition
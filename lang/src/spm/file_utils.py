import json
from os import path


def load_local_packages():

    with open("package.json", "r") as fp:
        packages = fp.read()

        return json.loads(packages)["packages"]

def load_solidity_file(file_path):
    with open(file_path.replace('"', ''), "r") as fp:
        input = fp.read()

        return input

def load_package(package_name, package_version, base_path = ''):
    package_path = path.join(base_path ,"{0}_{1}.json".format(package_name, package_version))
    with open(package_path, "r") as fp:
        package = fp.read()

        return json.loads(package)


def check_file_path(filePath):
    if not path.isfile(filePath.replace('"', '')):
        raise Exception(f"{filePath} is not correct file path")

def is_file(id):
    return id.startswith('".') and id.endswith('"')

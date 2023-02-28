import json
from os import path


def load_local_packages():

    with open("package.json", "r") as fp:
        packages = fp.read()

        return json.loads(packages)["packages"]

def load_solidity_file(file_path):
    with open(file_path.replace('"', ''), "r") as fp:
        input = fp.read()
        fp.seek(0)
        input_lines = fp.readlines()

        return input, input_lines

def load_package(package_name, package_version):
    with open("{0}_{1}.spm".format(package_name, package_version), "r") as fp:
        package = fp.read()

        return json.loads(package)


def check_file_path(filePath):
    if not path.isfile(filePath.replace('"', '')):
        raise Exception(f"{filePath} is not correct file path")

def is_file(id):
    return id.startswith('".') and id.endswith('"')
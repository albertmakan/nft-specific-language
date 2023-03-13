import json
from os import path


def load_local_packages():
    with open("package.json", "r") as fp:
        return json.load(fp)["packages"]

def load_solidity_file(file_path):
    with open(file_path.replace('"', ''), "r") as fp:
        return fp.read()

def load_package(package_name, package_version):
    with open(f"{package_name}_{package_version}.json", "r") as fp:
        return json.load(fp)

def check_file_path(filePath):
    if not path.isfile(filePath.replace('"', '')):
        raise Exception(f"{filePath} is not correct file path")

def is_file(id):
    return id.startswith('".') and id.endswith('"')

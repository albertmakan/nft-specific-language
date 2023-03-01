import json
import os

import requests

PACKAGE_JSON_PATH = "package.json"
SPM_PACKAGES_PATH = ".spm_packages"
SEARCH_INDEX_API_URL = "http://localhost:3000/api"
IPFS_NODE_URL = "http://localhost:9090/ipfs"

# Package Json utilities

def load_package_json():
  if not os.path.isfile(PACKAGE_JSON_PATH):
      raise Exception(f"{PACKAGE_JSON_PATH} does not exist.")
  
  with open(PACKAGE_JSON_PATH, "r") as fp:
    return json.loads(fp.read())

def save_package_json():
  with open(PACKAGE_JSON_PATH, "w") as fp:
    json.dump(package_json, fp, indent=4)


package_json = load_package_json()

# Install methods

def install_single_package(name, version):
  package = get_package(name, version)
  package["content"] = get_package_content(package)

  if is_package_installed(package):
    existing_package = {
      "name": package["name"],
      "version": package_json["packages"][package["name"]]
    }
    remove_existing_package(existing_package)

  save_package(package)
  package_json["packages"][package["name"]] = package["version"]
  save_package_json()


def install_from_package_json():
  for package_name, package_version in package_json["packages"].items():
    install_single_package(package_name, package_version)

# Some file system utilities

def is_package_installed(package):
  return package["name"] in package_json["packages"]

def save_package(package):
  if not os.path.isdir(SPM_PACKAGES_PATH):
    os.mkdir(SPM_PACKAGES_PATH)
    
  with open(form_package_path(package), "w") as fp:
    fp.write(package["content"])

def remove_existing_package(package):
  package_path = form_package_path(package)

  if os.path.isfile(package_path):
    os.remove(package_path)

def form_package_path(package):
  return f'{SPM_PACKAGES_PATH}/{package["name"]}_{package["version"]}.spm'

# Methods that are communicating with the search index and ipfs 

def get_package(package_name, version):
  if version == "latest":
    return get_latest_package(package_name)

  return get_specific_version_for_package(package_name, version)

def get_latest_package(package_name):
  response = requests.get(f"{SEARCH_INDEX_API_URL}/spm/search/" + package_name)
  if not response.ok:
      raise Exception(f"Package '{package_name}' does not exist.")
  
  responseObj = json.loads(response.text)
  if "name" not in responseObj and "version" not in responseObj:
     raise Exception(f"Package '{package_name}' does not exist.")

  return responseObj

def get_specific_version_for_package(package_name, package_version):
  response = requests.get(f"{SEARCH_INDEX_API_URL}/spm/package/" + package_name)
  if not response.ok:
     raise Exception(f"Package '{package_name}' does not exist.")
  
  packages = json.loads(response.text)
  for package in packages:
    if "version" in package and package["version"] == package_version:
      return package 

  raise Exception(f"Version '{package_version}' does not exist for package '{package_name}'.")

def get_package_content(package):
  response = requests.get(f'{IPFS_NODE_URL}/{package["cid"]}')

  return response.text


if __name__ == "__main__":
  
  # install_single("test_package", "latest")
  install_single_package("test_package2", "1.0.0")
  # install_from_package_json()
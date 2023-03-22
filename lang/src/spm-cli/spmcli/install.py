import json, os, requests
import click
from .constants import SPM_PACKAGES_PATH, SEARCH_INDEX_API_URL, IPFS_NODE_URL
from .package_json_utils import save_package_json, load_package_json


package_json = None

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
  save_package_json(package_json)

  print(f"{name}:{version} is installed.")


def install_from_package_json(use_latest):
  for package_name, package_version in package_json["packages"].items():
    if use_latest:
      install_single_package(package_name, "latest")
      continue

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
  return f'{SPM_PACKAGES_PATH}/{package["name"]}_{package["version"]}.json'

# Methods that are communicating with the search index and ipfs 

def get_package(package_name, version):
  if version == "latest":
    return get_latest_package(package_name)

  return get_specific_version_for_package(package_name, version)

def get_latest_package(package_name):
  response = requests.get(f"{SEARCH_INDEX_API_URL}/spm/search/" + package_name)
  if not response.ok:
    raise Exception(f"Package '{package_name}' does not exist.")

  packages = json.loads(response.text)
  if not len(packages):
    raise Exception(f"Package '{package_name}' does not exist.")

  package = packages[0]
  if "name" not in package and "version" not in package:
    raise Exception(f"Package '{package_name}' does not exist.")

  return package

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


@click.command()
@click.argument('name', default = '')
@click.option('--version', default = '')
def install(name, version):
  global package_json
  package_json = load_package_json()
  
  is_multi_install = len(name.strip()) == 0
  if is_multi_install and version != '' and version != 'latest':
    raise Exception ("Version cannot be provided when installing all packages.")
  
  if is_multi_install:
    use_latest = version == "latest"
    install_from_package_json(use_latest)
    return
  
  if version == '':
    version = "latest"

  install_single_package(name, version)

# Note: this is used for manual testing
if __name__ == "__main__":
  install()
  # install_single_package("test_package", "latest")
  # install_single_package("test_package2", "1.0.0")
  # install_from_package_json()
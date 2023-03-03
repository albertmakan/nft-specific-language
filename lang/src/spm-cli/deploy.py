
import click, json, os, requests
from constants import SEARCH_INDEX_API_URL
from package_json_utils import load_package_json, validate_package_metadata
from input_utils import take_input
from crypto import create_signature

@click.command()
def deploy():
  package_metadata = load_package_json()["metadata"]
  validate_package_metadata(package_metadata)
  package_content = load_package_content(f'{package_metadata["name"]}.spm')

  priv_key = take_input("Package private key")
  signature = create_signature(priv_key, package_metadata["name"] + package_metadata["author"] + package_metadata["version"])

  data = {
    "name": package_metadata["name"],
    "author": package_metadata["author"],
    "version": package_metadata["version"],
    "content": package_content,
    "pubkey": package_metadata["pubkey"],
    "signature": signature
  }

  package_result = deploy_package(data)
  if (package_result):
    print(f'Succefully deployed package {data["name"]}:{data["version"]}')


def load_package_content(package_path):
  if not os.path.isfile(package_path):
    raise Exception(f"{package_path} cannot be found.")
  
  with open(package_path, "r") as fp:
    return fp.read()


def deploy_package(package_data):

  response = requests.post(f"{SEARCH_INDEX_API_URL}/spm/packages", json = package_data)
  responseObj = json.loads(response.text)
  if not response.ok:
    raise Exception(f"Failed to deploy package due to: '{responseObj['message']}'")

  return True


if __name__ == "__main__":
  deploy()
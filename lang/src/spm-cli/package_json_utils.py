
import json, os
from constants import PACKAGE_JSON_PATH
from validation_utils import is_version_valid


def load_package_json():
  if not os.path.isfile(PACKAGE_JSON_PATH):
    raise Exception(f"{PACKAGE_JSON_PATH} does not exist.")
  
  with open(PACKAGE_JSON_PATH, "r") as fp:
    return json.loads(fp.read())


def save_package_json(package_json):
  with open(PACKAGE_JSON_PATH, "w") as fp:
    json.dump(package_json, fp, indent=4)


def validate_package_metadata(metadata):
  
  if "name" not in metadata or _is_empty(metadata["name"]):
    raise Exception("Package name cannot be empty")

  if "author" not in metadata or _is_empty(metadata["author"]):
    raise Exception("Package author cannot be empty")

  if "version" not in metadata or not is_version_valid(metadata["version"]):
    raise Exception("Package version must be Major.Minor.Patch")

  if "pubkey" not in metadata or _is_empty(metadata["pubkey"]):
    raise Exception("Package public key cannot be empty")

def _is_empty(text):
  return text is not None and len(text.strip()) == 0

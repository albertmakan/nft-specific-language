
import json
import os
import requests


SEARCH_INDEX_API_URL = "http://localhost:3000/api"


def load_package_content(package_path):
  if not os.path.isfile(package_path):
    raise Exception(f"{package_path} cannot be found.")
  
  with open(package_path, "r") as fp:
    return fp.read()

def push_package(package_data):

  response = requests.post(f"{SEARCH_INDEX_API_URL}/spm/packages", json = package_data)
  if response.ok:
    responseObj = json.loads(response.text)
    print(responseObj)
    return responseObj
  else:
    print(response.text)


if __name__ == "__main__":
  package_content = load_package_content("test.py")

  data = {
    "name": "test_package2",
    "version": "1.0.0",
    "author": "Milos Panic",
    "pubkey": "MILOSPANICCCCCCCCCCCCCCCCCCCCC",
    "content": package_content
  }

  push_package(data)
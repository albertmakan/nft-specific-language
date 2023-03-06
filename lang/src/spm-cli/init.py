import os, json, click
from jinja2 import Environment, BaseLoader
from input_utils import take_input
from validation_utils import is_version_valid
from constants import SPM_PACKAGES_PATH, PACKAGE_JSON_PATH
from crypto import generate_key_pair


initial_package_template = '''
packages {
  // using standards.erc721 as ERC721
  // using "./erc20.sol" as ERC20
}

package {{name}}
{
  
}
'''

@click.command()
def init():
  name, author, version = read_package_data()
  priv_key, pub_key = generate_key_pair()

  create_spm_packages()
  create_package_definition(name)
  create_package_json(name, author, version, pub_key)

  print('{:*^64}'.format(' MAKE SURE TO SAVE PRIVATE KEY '))
  print(priv_key)


def create_spm_packages():
  if not os.path.exists(SPM_PACKAGES_PATH):
    os.makedirs(SPM_PACKAGES_PATH)

def create_package_definition(name):
  environment = Environment(loader=BaseLoader)
  template = environment.from_string(initial_package_template)
 
  filename = f"{name}.spm"
  content = template.render(
    name = name,
  )  

  with open(filename, "w") as fp:
    fp.write(content)

def create_package_json(name, author, version, pub_key):
  if os.path.exists(PACKAGE_JSON_PATH):
    return
  
  init_content = {
    "metadata": {
      "name": name,
      "author": author,
      "version": version,
      "pubkey": pub_key
    },
    "packages": {
    
    }
  }

  with open(PACKAGE_JSON_PATH, "w") as fp:
    fp.write(json.dumps(init_content, sort_keys=True, indent=4))


def read_package_data():
  name = take_input("Package name")
  author = take_input("Package author")
  
  while True:
    version = take_input("Package version", "0.0.1")
    if is_version_valid(version):
      break
    print("The prefered version format is: Major.Minor.Patch, where each part is a whole number.")

  return name, author, version

# Note: this is used for manual testing
if __name__ == "__main__":
  init()
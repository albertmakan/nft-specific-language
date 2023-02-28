import json
import os
from jinja2 import Environment, FileSystemLoader

def init(name, author):
  create_spm_packages()
  create_package_json(name, author)
  create_package_definition(name)

def create_spm_packages():
  if not os.path.exists("./.spm_packages"):
    os.makedirs("./.spm_packages")
    
def create_package_json(name, author):
  if os.path.exists("./package.json"):
    return
  
  init_content = {
    "metadata": {
      "name": name,
      "author": author
    },
    "packages": {
    
    }
  }

  with open("./package.json", "w") as fp:
    fp.write(json.dumps(init_content, sort_keys=True, indent=4))

def create_package_definition(name):
  environment = Environment(loader=FileSystemLoader("./"))
  template = environment.get_template("template.spm")
 
  filename = f"{name}.spm"
  content = template.render(
    name = name,
  )  

  with open(filename, "w") as fp:
    fp.write(content)

if __name__ == "__main__":
  init("proba", "milos")
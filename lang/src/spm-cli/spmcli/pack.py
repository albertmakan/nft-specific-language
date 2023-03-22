import click, os
from .package_json_utils import load_package_json


@click.command()
def pack():
  package_metadata = load_package_json()["metadata"]

  package_file = f'{package_metadata["name"]}.spm'
  output_file = f'{package_metadata["name"]}.json'
  os.system(f"textx generate {package_file} --target json --output-path {output_file}")

# Note: this is used for manual testing
if __name__ == "__main__":
  pack()
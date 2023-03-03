import click
from validation_utils import is_version_valid
from package_json_utils import load_package_json, save_package_json, validate_package_metadata

package_json = None
package_metadata = None

@click.command()
@click.argument('version', default = '')
@click.option('--reset', default = False)
def version(version, reset):
  global package_json, package_metadata
  package_json = load_package_json()
  package_metadata = package_json["metadata"]
  validate_package_metadata(package_metadata)

  version = version.strip()

  if reset:
    handle_reset(version)
    return
  
  if len(version) == 0:
    print_current_version()
    return

  if version.lower() in ['major', 'minor', 'patch']:
    version = increase_version_part(package_metadata["version"], version_part = version)

  save_new_version(version)
  print_current_version()


def handle_reset(version):
  initial_version = version
  if len(version) == 0:
    version = "0.0.0"

  if version.lower() in ['major', 'minor', 'patch']:
    version = reset_version_part(package_metadata["version"], version_part = version)
    
  if initial_version != version:
    save_new_version(version)
    print_current_version()
    return
  
  raise Exception("Cannot use --reset with custom version set")


def increase_version_part(version, version_part):
  version_part_indexes = {
    "major": 0,
    "minor": 1,
    "patch": 2
  }

  version_parts = version.split('.')
  version_part_index = version_part_indexes[version_part]
  version_parts[version_part_index] = str(int(version_parts[version_part_index]) + 1)

  return '.'.join(version_parts)

def reset_version_part(version, version_part):
  version_part_indexes = {
    "major": 0,
    "minor": 1,
    "patch": 2
  }

  version_parts = version.split('.')
  version_part_index = version_part_indexes[version_part]
  version_parts[version_part_index] = '0'

  return '.'.join(version_parts)


def print_current_version():
  name, version = package_metadata["name"], package_metadata["version"] 
  print(f"{name}:{version}")

def save_new_version(version):
  if not is_version_valid(version):
    raise Exception("Version must be Major.Minor.Patch")

  package_metadata["version"] = version
  save_package_json(package_json)


if __name__ == "__main__":
  version()
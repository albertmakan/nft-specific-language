import os
import shutil
import click
from .constants import *

templates_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "templates")


@click.command()
@click.argument('name')
def init(name: str):
    shutil.copy2(os.path.join(templates_path, 'test.spl'), f'{name}{SPL}')
    print(f'{name}{SPL} is created')

    if not os.path.exists(SPM_PACKAGES_PATH):
        os.makedirs(SPM_PACKAGES_PATH)
        print(f'{SPM_PACKAGES_PATH} is created')

    shutil.copy2(os.path.join(templates_path, 'std_1.0.0.json'),
                 SPM_PACKAGES_PATH)

    shutil.copy2(os.path.join(templates_path, 'package.json'), '.')

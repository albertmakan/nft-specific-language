import os
import click
from .constants import SPL


@click.command()
@click.argument('names', nargs=-1)
def combine(names: list):
    if not names:
        names = [f.removesuffix(SPL)
                 for f in os.listdir() if f.endswith(SPL)]
    if not names:
        print("Nothing to combine")
    for name in names:
        os.system(f"textx generate {name}{SPL} --target sol -o {name}.sol")

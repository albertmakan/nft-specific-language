import os
from spl import Script
from textx import generator

__version__ = "0.1.0.dev"


@generator('spl', 'sol')
def spl_generate_sol(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating sol from spl descriptions"

    output_file = "proba1"
    generator_callback(model, output_file, overwrite)


def generator_callback(model: Script, output_file: str, overwrite: bool):
    """
    A generator function that produce output_file from model.
    """
    # TODO: Write here code that produce generated output
    with open(output_file, 'w') as f:
        f.write(str(model))
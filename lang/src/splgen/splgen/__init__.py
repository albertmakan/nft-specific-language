import os
from functools import partial
from textx import generator, gen_file, get_output_filename

__version__ = "0.1.0.dev"


@generator('spl', 'sol')
def spl_generate_sol(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating sol from spl descriptions"

    output_file = get_output_filename(model.file_name, output_path, '*.spl')
    gen_file(model.file_name, output_file,
             partial(generator_callback, model, output_file),
             overwrite,
             success_message='To convert to png run "dot -Tpng -O {}"'
             .format(os.path.basename(output_file)))


def generator_callback(model, output_file):
    """
    A generator function that produce output_file from model.
    """
    # TODO: Write here code that produce generated output
import os
from obj_processors import contract_admin_processor, method_processor, package_processor, percent_processor, contract_processor
from textx import language, metamodel_from_file

from model import *

__version__ = "0.1.0.dev"

_classes = (Parameter, Parameters, Administrator, AdministrationSection, Method, ContractAdministrator,
            ContractImplementation, ContractDefinition, ContractSection, PackageImport, PackageSection, Script, AddressSet, Percentage, Address)


@language('spl', '*.spl')
def spl_language():
    "spl language"
    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'spl.tx'), classes=_classes)
    mm.register_obj_processors({
        'PackageSection': package_processor,
        'Method': method_processor,
        'Percentage': percent_processor,
        'ContractDefinition': contract_processor,
        'ContractAdministrator': contract_admin_processor
    })

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/

    return mm

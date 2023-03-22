import os
from textx import language, metamodel_from_file

from .obj_processors import package_import_processor, package_import_section_processor, package_export_section_processor, package_export_processor
from .model import *

__version__ = "0.1.0.dev"

_classes = (PackageImport, PackageImportSection, PackageExport, PackageExportSection, Script)


@language('spm', '*.spm')
def spm_language():
    "spm language"
    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'spm.tx'), classes=_classes)
    mm.register_obj_processors({
        'PackageImportSection': package_import_section_processor,
        'PackageImport': package_import_processor,
        'PackageExportSection': package_export_section_processor,
        'PackageExport': package_export_processor,
    })

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/

    return mm

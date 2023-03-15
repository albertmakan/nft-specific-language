import os
from textx import metamodel_from_file
from model import *
from obj_processors import change_base_path, change_local_packages, package_import_processor, package_import_section_processor, package_export_section_processor, package_export_processor

_classes = (PackageImport, PackageImportSection, PackageExport, PackageExportSection, Script)

def create_mm():
    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir,"spm.tx"),classes=_classes)
    mm.register_obj_processors({
    'PackageImportSection': package_import_section_processor,
    'PackageImport': package_import_processor,
    'PackageExportSection': package_export_section_processor,
    'PackageExport': package_export_processor,
    })
    mm.skip_errors = True
    return mm

def change_packages(packages):
    change_local_packages(packages)

def change_path(path):
    change_base_path(path)
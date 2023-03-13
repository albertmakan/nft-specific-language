from typing import Any, Optional, List
from dataclasses import dataclass


@dataclass
class Construct:
    parent: Any

@dataclass
class PackageImport(Construct):
    id: str
    alias: str
    data: Optional[Any]

@dataclass
class PackageImportSection(Construct):
    packages: List[PackageImport]

@dataclass
class PackageExport(Construct):
    package_name: str
    exports: List
    export_type: str
    export_name: str
    export_alias: str

@dataclass
class PackageExportSection(Construct):
    name: str
    exports: List[PackageExport]

@dataclass
class Script:
    imports: PackageImportSection
    package: PackageExportSection
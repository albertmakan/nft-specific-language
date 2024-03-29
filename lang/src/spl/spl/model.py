from typing import Any, List, Union
from dataclasses import dataclass

@dataclass
class Construct:
    parent: Any


@dataclass
class Address(Construct):
    value: str
    def __str__(self) -> str:
        return str(self.value)

@dataclass
class AddressSet(Construct):
    values: List[Address]
    def __str__(self) -> str:
        return str(self.values)

@dataclass
class Percentage(Construct):
    percent: int
    def __str__(self) -> str:
        return f"{self.percent}%"

@dataclass
class Parameter(Construct):
    literal: Union[str, int, float, AddressSet, Percentage, Address]
    name: str

@dataclass
class Parameters(Construct):
    parameters: List[Parameter]

@dataclass
class Method(Construct):
    name: str
    params: Parameters

@dataclass
class ContractImplementation(Construct):
    methods: List[Method]

@dataclass
class ContractDefinition(Construct):
    name: str
    implementation: ContractImplementation

@dataclass
class ContractSection(Construct):
    contracts: List[ContractDefinition]

@dataclass
class PackageImport(Construct):
    id: str
    alias: str

@dataclass
class PackageSection(Construct):
    packages: List[PackageImport]

@dataclass
class ContractAdministrator(Construct):
    contract: ContractDefinition
    methods: List[Method]

@dataclass
class Administrator(Construct):
    method: Method
    contract_administrators: List[ContractAdministrator]

@dataclass
class AdministrationSection(Construct):
    main_administrator: Administrator
    extension_administrators: List[Administrator]

@dataclass
class Script:
    package_section: PackageSection
    contract_section: ContractSection
    administration: AdministrationSection

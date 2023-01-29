from solcx import compile_source, install_solc
install_solc('v0.4.25')

# validator za sintaksu target jezika (Solidity)
print(compile_source("contract Foo { function Foo() {} }")["<stdin>:Foo"]["opcodes"])

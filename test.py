from asm import load_asm
from vm import get_vm

prog = load_asm('test.asm')
vm = get_vm()
vm.load_symbols(prog["labels"])
vm.load_program(prog["lines"])
while not(vm.stop):
    vm.step()

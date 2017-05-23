from vm import vmop
from xcp import xcp_call

def get_index(reg):
    return int(reg.split(".")[-1])

def get_reg_name_idx(reg):
    sp = reg.split(".")
    return sp[0], int(sp[1])

@vmop
def op_clear(vm, reg):
    if reg in ("z", "line"):
        vm.regs[reg] = 0
    elif reg in ("ob", "list"):
        vm.regs[reg] = [None, None, None, None, None, None, None, None]
    elif reg.startswith("int."):
        vm.regs["int"][get_index(reg)] = 0
    elif reg.startswith("list."):
        vm.regs["list"][get_index(reg)] = None
    elif reg.startswith("ob."):
        vm.regs["ob"][get_index(reg)] = None
    elif reg in ("table", "filterop"):
        vm.regs[reg] = None
    elif reg == "filter":
        vm.regs[reg] = {}
    elif reg == "filters":
        vm.regs[reg] = []

@vmop
def op_filterop(vm, op):
    vm.regs["filterop"] = op

@vmop
def op_table(vm, table):
    vm.regs["table"] = table

@vmop
def op_filter(vm, field, value):
    vm.regs["filter"][field] = value

@vmop
def op_push(vm, concept):
    if concept == "filter":
        vm.regs["filters"].append(vm.regs["filter"])
        vm.regs["z"] = len(vm.regs["filters"])

@vmop
def op_get_table(vm, reg):
    list_idx = get_index(reg)
    ops = {}
    if len(vm.regs["filters"]) > 0:
        ops["filters"] = vm.regs["filters"]
    lst = xcp_call("get_%s" % vm.regs["table"], ops)
    vm.regs["list"][list_idx] = lst

@vmop
def op_load_len(vm, lst, reg):
    list_idx = get_index(lst)
    reg_idx = get_index(reg)

    vm.regs["int"][reg_idx] = len(vm.regs["list"][list_idx])

@vmop
def op_rlcmp(vm, reg, lit):
    lit = int(lit)
    reg_name, reg_idx = get_reg_name_idx(reg)
    regv = vm.regs[reg_name][reg_idx]

    if regv < lit:
        vm.regs["z"] = -1
    elif regv > lit:
        vm.regs["z"] = 1
    else:
        vm.regs["z"] = 0

@vmop
def op_jz(vm, label):
    if vm.regs["z"] == 0:
        vm.regs["line"] = vm.syms[label]

@vmop
def op_jnz(vm, label):
    if vm.regs["z"] != 0:
        vm.regs["line"] = vm.syms[label]

@vmop
def op_rlsum(vm, reg, lit):
    reg_name, reg_idx = get_reg_name_idx(reg)
    vm.regs["z"] = vm.regs[reg_name][reg_idx] + int(lit)

@vmop
def op_movr(vm, reg):
    reg_name, reg_idx = get_reg_name_idx(reg)
    vm.regs[reg_name][reg_idx] = vm.regs["z"]

@vmop
def op_loadob(vm, lit, lst):
    reg_name, reg_idx = get_reg_name_idx(lst)
    curlst = vm.regs[reg_name][reg_idx]
    ob = curlst[vm.regs["z"]]
    vm.regs["ob"][int(lit)] = ob

@vmop
def op_call(vm, label):
    vm.regs["stack"].append(vm.regs["line"])
    vm.regs["line"] = vm.syms[label]

@vmop
def op_return(vm):
    vm.regs["line"] = vm.regs["stack"].pop()

@vmop
def op_jmp(vm, label):
    vm.regs["line"] = vm.syms[label]

@vmop
def op_obcmp(vm, idx, field, value):
    print(vm.regs["ob"][int(idx)])
    fval = vm.regs["ob"][int(idx)][field]

    if fval == value:
        vm.regs["z"] = 0
    elif fval < value:
        vm.regs["z"] = -1
    elif fval > value:
        vm.regs["z"] = 1

@vmop
def op_throw(vm, error):
    raise error

@vmop
def op_finish(vm):
    vm.stop = True

@vmop
def op_print(vm, st):
    print("DEBUG: %s" % st)

def get_byte_ops():
    return {
        "clear": op_clear,
        "filterop": op_filterop,
        "table": op_table,
        "filter": op_filter,
        "push": op_push,
        "get_table": op_get_table,
        "load_len": op_load_len,
        "rlcmp": op_rlcmp,
        "jz": op_jz,
        "jnz": op_jnz,
        "jmp": op_jmp,
        "rlsum": op_rlsum,
        "movr": op_movr,
        "loadob": op_loadob,
        "call": op_call,
        "return": op_return,
        "obcmp": op_obcmp,
        "throw": op_throw,
        "finish": op_finish,
        "print": op_print
    }


_vm_singleton_ = None

class VM(object):
    def __init__(self):
        self.regs = {
            "filter": {},
            "filters": [],
            "filterop": None,
            "table": None,
            "ob": [None, None, None, None, None, None, None, None],
            "list": [None, None, None, None, None, None, None, None],
            "int": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "z": 0,
            "line": 0,
            "stack": []
        }

        self.syms = {}
        self.prog = []
        self.stop = False

    def load_symbols(self, syms):
        self.syms = syms

    def load_program(self, prog):
        self.prog = prog

    def step(self):
        if not(self.stop):
            lineno = self.regs["line"]
            op = self.prog[lineno]
            self.regs["line"] += 1

            if op != None:
                print("%i: %s" % (lineno, op.__name__))
                op()

class vmop(object): # This is a function decorator for VM ops
    def __init__(self, f):
        self.f = f

    def __call__(self, cs_args):
        ret = None
        if len(cs_args) > 0:
            args = cs_args.split(",")
            ret = lambda: self.f(_vm_singleton_, *args)
        else:
            ret = lambda: self.f(_vm_singleton_)

        ret.__name__ =  self.f.__name__

        return ret

def get_vm():
    return _vm_singleton_

_vm_singleton_ = VM()

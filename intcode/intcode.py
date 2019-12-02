class Program():
    OPCODES = {
        1: lambda s: s._threearg_opcode(lambda a, b: a + b),
        2: lambda s: s._threearg_opcode(lambda a, b: a * b),
        99: lambda s: True
    }

    def __init__(self, initial_memory):
        self._pc = 0
        self._memory = initial_memory.copy()

    @property
    def pc(self):
        return self._pc

    @property
    def memory(self):
        return self._memory

    def _threearg_opcode(self, resultfn):
        arg1 = self._memory[self._pc + 1]
        arg2 = self._memory[self._pc + 2]
        dest = self._memory[self._pc + 3]

        value1 = self._memory[arg1]
        value2 = self._memory[arg2]

        self._memory[dest] = resultfn(value1, value2)
        self._pc += 4
        return False

    def single_step(self):
        opcode = self._memory[self._pc]

        try:
            opcodefn = self.OPCODES[opcode]
        except KeyError:
            raise UnknownOpcodeException(opcode)

        return opcodefn(self)

    def run(self):
        terminated = False
        while not terminated:
            terminated = self.single_step()

class UnknownOpcodeException(Exception):
    def __init__(self, opcode):
        self._opcode = opcode

    @property
    def opcode(self):
        return self._opcode

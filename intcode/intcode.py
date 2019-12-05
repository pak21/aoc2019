class Program():
    OPCODES = {
        1: lambda s, m: s._threearg_opcode(m, lambda a, b: a + b),
        2: lambda s, m: s._threearg_opcode(m, lambda a, b: a * b),
        3: lambda s, m: s._input(m[0]),
        4: lambda s, m: s._output(m[0]),
        5: lambda s, m: s._jump_if_true(m),
        6: lambda s, m: s._jump_if_false(m),
        7: lambda s, m: s._threearg_opcode(m, lambda a, b: 1 if a < b else 0),
        8: lambda s, m: s._threearg_opcode(m, lambda a, b: 1 if a == b else 0),
        99: lambda s, m: True
    }

    def __init__(self, initial_memory, input_value = 0):
        self._pc = 0
        self._outputs = []
        self._memory = initial_memory.copy()
        self._input_value = input_value

    @property
    def pc(self):
        return self._pc

    @property
    def memory(self):
        return self._memory

    @property
    def outputs(self):
        return self._outputs

    def _threearg_opcode(self, modes, resultfn):
        arg1 = self._memory[self._pc + 1]
        arg2 = self._memory[self._pc + 2]
        dest = self._memory[self._pc + 3]

        value1 = self._memory[arg1] if modes[0] == 0 else arg1
        value2 = self._memory[arg2] if modes[1] == 0 else arg2

        result = resultfn(value1, value2)

        self._memory[dest] = result
        self._pc += 4
        return False

    def _input(self, mode):
        arg1 = self._memory[self._pc + 1]
        self._memory[arg1] = self._input_value
        self._pc += 2
        return False

    def _output(self, mode):
        arg1 = self._memory[self._pc + 1]
        value1 = self._memory[arg1] if mode == 0 else arg1
        self._outputs.append(value1)
        self._pc += 2
        return False

    def _jump_if_true(self, modes):
        arg1 = self._memory[self._pc + 1]
        arg2 = self._memory[self._pc + 2]

        value1 = self._memory[arg1] if modes[0] == 0 else arg1
        value2 = self._memory[arg2] if modes[1] == 0 else arg2

        if value1 != 0:
            self._pc = value2
        else:
            self._pc += 3

    def _jump_if_false(self, modes):
        arg1 = self._memory[self._pc + 1]
        arg2 = self._memory[self._pc + 2]

        value1 = self._memory[arg1] if modes[0] == 0 else arg1
        value2 = self._memory[arg2] if modes[1] == 0 else arg2

        if value1 == 0:
            self._pc = value2
        else:
            self._pc += 3

    def single_step(self):
        value = self._memory[self._pc]
        opcode = value % 100
        p1mode = (value // 100) % 10
        p2mode = (value // 1000) % 10
        p3mode = (value // 10000) % 10
        modes = [p1mode, p2mode, p3mode]

        try:
            opcodefn = self.OPCODES[opcode]
        except KeyError:
            raise UnknownOpcodeException(opcode)

        return opcodefn(self, modes)

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

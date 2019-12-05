class Program():
    OPCODES2 = {
        4: (1, lambda s, p: s._output(p)),
    }

    OPCODES = {
        1: lambda s, m: s._threearg_opcode(m, lambda a, b: a + b),
        2: lambda s, m: s._threearg_opcode(m, lambda a, b: a * b),
        3: lambda s, m: s._input(),
        4: lambda s, m: s._output(m),
        5: lambda s, m: s._jump(m, lambda a: a != 0),
        6: lambda s, m: s._jump(m, lambda a: a == 0),
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

    def _get_parameters(self, modes, count):
        args = self._memory[self._pc + 1:self._pc + 1 + count]
        parameters = [args[i] if modes[i] else self._memory[args[i]] for i in range(count)]
        return parameters

    def _threearg_opcode(self, modes, resultfn):
        parameters = self._get_parameters(modes, 2)
        dest = self._memory[self._pc + 3]

        result = resultfn(parameters[0], parameters[1])

        self._memory[dest] = result
        self._pc += 4
        return False

    def _input(self):
        arg1 = self._memory[self._pc + 1]
        self._memory[arg1] = self._input_value
        self._pc += 2
        return False

    def _output(self, parameters):
        self._outputs.append(parameters[0])
        return False

    def _jump(self, modes, testfn):
        parameters = self._get_parameters(modes, 2)
        self._pc = parameters[1] if testfn(parameters[0]) else self._pc + 3
        return False

    def single_step(self):
        value = self._memory[self._pc]
        opcode = value % 100
        p1mode = (value // 100) % 10
        p2mode = (value // 1000) % 10
        p3mode = (value // 10000) % 10
        modes = [p1mode, p2mode, p3mode]

        if opcode in self.OPCODES2:
            param_count, opcodefn = self.OPCODES2[opcode]
            params = self._get_parameters(modes, param_count)
            self._pc += 1 + param_count
            return opcodefn(self, params)
        else:
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

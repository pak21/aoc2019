class Program():
    OPCODES = {
        1: (3, lambda s, p: s._threearg_opcode(p, lambda a, b: a + b)),
        2: (3, lambda s, p: s._threearg_opcode(p, lambda a, b: a * b)),
        3: (1, lambda s, p: s._input()),
        4: (1, lambda s, p: s._output(p)),
        5: (2, lambda s, p: s._jump(p, lambda a: a != 0)),
        6: (2, lambda s, p: s._jump(p, lambda a: a == 0)),
        7: (3, lambda s, p: s._threearg_opcode(p, lambda a, b: 1 if a < b else 0)),
        8: (3, lambda s, p: s._threearg_opcode(p, lambda a, b: 1 if a == b else 0)),
        99: (0, lambda s, p: True)
    }

    def __init__(self, initial_memory, input_value = None, *, input_values = None):
        self._pc = 0
        self._outputs = []
        self._memory = initial_memory.copy()
        if input_values is not None:
            self._input_values = input_values
        elif input_value is not None:
            self._input_values = [input_value]

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

    def _threearg_opcode(self, parameters, resultfn):
        result = resultfn(parameters[0], parameters[1])
        dest = self._memory[self._pc - 1] # PC has already been incremented
        self._memory[dest] = result
        return False

    def _input(self):
        dest = self._memory[self._pc - 1] # PC has already been incremented
        self._memory[dest] = self._input_values.pop(0)
        return False

    def _output(self, parameters):
        self._outputs.append(parameters[0])
        return False

    def _jump(self, parameters, testfn):
        if testfn(parameters[0]):
            self._pc = parameters[1]
        return False

    def single_step(self):
        value = self._memory[self._pc]
        opcode = value % 100
        p1mode = (value // 100) % 10
        p2mode = (value // 1000) % 10
        p3mode = (value // 10000) % 10
        modes = [p1mode, p2mode, p3mode]

        try:
            param_count, opcodefn = self.OPCODES[opcode]
        except KeyError:
            raise UnknownOpcodeException(opcode)

        params = self._get_parameters(modes, param_count)
        self._pc += 1 + param_count
        return opcodefn(self, params)

    def run(self):
        terminated = False
        while not terminated:
            terminated = self.single_step()

    def run_to_output(self):
        terminated = False
        outputs_length = len(self._outputs)
        while not terminated and len(self._outputs) == outputs_length:
            terminated = self.single_step()

class UnknownOpcodeException(Exception):
    def __init__(self, opcode):
        self._opcode = opcode

    @property
    def opcode(self):
        return self._opcode

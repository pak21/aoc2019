import collections

class Program():
    OPCODES = {
        1: (2, 1, lambda s, p: s._threearg_opcode(p, lambda a, b: a + b)),
        2: (2, 1, lambda s, p: s._threearg_opcode(p, lambda a, b: a * b)),
        3: (0, 1, lambda s, p: s._input(p[0])),
        4: (1, 0, lambda s, p: s._output(p)),
        5: (2, 0, lambda s, p: s._jump(p, lambda a: a != 0)),
        6: (2, 0, lambda s, p: s._jump(p, lambda a: a == 0)),
        7: (2, 1, lambda s, p: s._threearg_opcode(p, lambda a, b: 1 if a < b else 0)),
        8: (2, 1, lambda s, p: s._threearg_opcode(p, lambda a, b: 1 if a == b else 0)),
        9: (1, 0, lambda s, p: s._adjust_relative_base(p[0])),
        99: (0, 0, lambda s, p: True)
    }

    def __init__(self, initial_memory, input_value = None, *, input_values = None, input_generator = None):
        self._pc = 0
        self._relative_base = 0
        self._outputs = []
        self._memory = collections.defaultdict(int)

        for k, v in enumerate(initial_memory):
            self._memory[k] = v

        if input_generator is not None:
            self._input_iterator = input_generator()
        elif input_values is not None:
            self._input_iterator = iter(input_values)
        elif input_value is not None:
            self._input_iterator = iter([input_value])

    @property
    def pc(self):
        return self._pc

    @property
    def relative_base(self):
        return self._relative_base

    @property
    def memory(self):
        max_index = max(self._memory.keys())
        memory = [0] * (max_index + 1)
        for k, v in self._memory.items():
            memory[k] = v
        return memory

    @property
    def outputs(self):
        return self._outputs

    def _get_parameter(self, mode, argument):
        if mode == 0:
            # Position mode
            parameter = self._memory[argument]
        elif mode == 1:
            # Immediate mode
            parameter = argument
        elif mode == 2:
            # Relative mode
            parameter = self._memory[self._relative_base + argument]
        else:
            raise InvalidAddressingModeException(mode, False)

        return parameter

    def _get_output_parameter(self, mode, argument):
        if mode == 0:
            # Position mode
            parameter = argument
        elif mode == 1:
            # Output parameters cannot be in immediate mode
            raise InvalidAddressingModeException(mode, True)
        elif mode == 2:
            # Relative mode
            parameter = self._relative_base + argument
        else:
            raise InvalidAddressingModeException(mode, True)

        return parameter

    def _get_parameters(self, modes, count):
        args = [self._memory[i] for i in range(self._pc + 1, self._pc + 1 + count)]
        parameters = [self._get_parameter(modes[i], args[i]) for i in range(count)]
        return parameters

    def _get_output_parameters(self, modes, input_count, output_count):
        args = [self._memory[i] for i in range(self._pc + 1 + input_count, self._pc + 1 + input_count + output_count)]
        parameters = [self._get_output_parameter(modes[input_count + i], args[i]) for i in range(output_count)]
        return parameters

    def _threearg_opcode(self, parameters, resultfn):
        result = resultfn(parameters[0], parameters[1])
        self._memory[parameters[2]] = result
        return False

    def _input(self, parameter):
        self._memory[parameter] = next(self._input_iterator)
        return False

    def _output(self, parameters):
        self._outputs.append(parameters[0])
        return False

    def _jump(self, parameters, testfn):
        if testfn(parameters[0]):
            self._pc = parameters[1]
        return False

    def _adjust_relative_base(self, parameter):
        self._relative_base += parameter
        return False

    def single_step(self):
        value = self._memory[self._pc]
        opcode = value % 100
        p1mode = (value // 100) % 10
        p2mode = (value // 1000) % 10
        p3mode = (value // 10000) % 10
        modes = [p1mode, p2mode, p3mode]

        try:
            input_param_count, output_param_count, opcodefn = self.OPCODES[opcode]
        except KeyError:
            raise UnknownOpcodeException(opcode)

        param_count = input_param_count + output_param_count
        input_params = self._get_parameters(modes, input_param_count)
        output_params = self._get_output_parameters(modes, input_param_count, output_param_count)
        params = input_params + output_params
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

class InvalidAddressingModeException(Exception):
    def __init__(self, addressing_mode, output_mode):
        self._addressing_mode = addressing_mode
        self._output_mode = output_mode

    @property
    def addressing_mode(self):
        return self._addressing_mode

    @property
    def output_mode(self):
        return self._output_mode

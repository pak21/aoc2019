import collections

class Program():
    OPCODES = {
        1: (2, 1, lambda s, p: s._threearg_opcode(p, lambda a, b: a + b)),
        2: (2, 1, lambda s, p: s._threearg_opcode(p, lambda a, b: a * b)),
        3: (0, 1, lambda s, p: s._input(p[0])),
        4: (1, 0, lambda s, p: s._output(p[0])),
        5: (2, 0, lambda s, p: s._jump(p, lambda a: a != 0)),
        6: (2, 0, lambda s, p: s._jump(p, lambda a: a == 0)),
        7: (2, 1, lambda s, p: s._threearg_opcode(p, lambda a, b: 1 if a < b else 0)),
        8: (2, 1, lambda s, p: s._threearg_opcode(p, lambda a, b: 1 if a == b else 0)),
        9: (1, 0, lambda s, p: s._adjust_relative_base(p[0])),
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

    def _get_parameter(self, mode, argument, is_output_parameter):
        if mode < 0 or mode > 2:
            raise InvalidAddressingModeException(mode, is_output_parameter)

        # Output parameters cannot be in immediate mode
        if is_output_parameter and mode == 1:
            raise InvalidAddressingModeException(mode, is_output_parameter)

        # Relative mode
        if mode == 2:
            argument += self._relative_base

        # Automatically derefence input parameters _not_ in immediate mode
        if not is_output_parameter and mode != 1:
            argument = self._memory[argument]

        return argument

    def _get_parameters(self, modes, offset, count, getfn):
        args_base = self._pc + 1 + offset
        args = [self._memory[i] for i in range(args_base, args_base + count)]
        return [getfn(*pair) for pair in zip(modes, args)]

    def _threearg_opcode(self, parameters, resultfn):
        result = resultfn(parameters[0], parameters[1])
        self._memory[parameters[2]] = result

    def _input(self, parameter):
        self._memory[parameter] = next(self._input_iterator)

    def _output(self, parameter):
        self._outputs.append(parameter)

    def _jump(self, parameters, testfn):
        if testfn(parameters[0]):
            self._pc = parameters[1]

    def _adjust_relative_base(self, parameter):
        self._relative_base += parameter

    def single_step(self):
        value = self._memory[self._pc]
        opcode = value % 100
        p1mode = (value // 100) % 10
        p2mode = (value // 1000) % 10
        p3mode = (value // 10000) % 10
        modes = [p1mode, p2mode, p3mode]

        if opcode == 99: # Terminate
            return True

        try:
            input_param_count, output_param_count, opcodefn = self.OPCODES[opcode]
        except KeyError:
            raise UnknownOpcodeException(opcode)

        input_params = self._get_parameters(modes, 0, input_param_count, lambda m, a: self._get_parameter(m, a, False))
        output_params = self._get_parameters(modes[input_param_count:], input_param_count, output_param_count, lambda m, a: self._get_parameter(m, a, True))
        self._pc += 1 + input_param_count + output_param_count
        opcodefn(self, input_params + output_params)

        return False # Haven't terminated

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

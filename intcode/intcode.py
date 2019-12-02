class Program():
    def __init__(self, initial_memory):
        self._pc = 0
        self._memory = initial_memory.copy()

    @property
    def pc(self):
        return self._pc

    @property
    def memory(self):
        return self._memory

    def single_step(self):
        arg1 = self.memory[self._pc + 1]
        arg2 = self.memory[self._pc + 2]
        dest = self.memory[self._pc + 3]

        value1 = self.memory[arg1]
        value2 = self.memory[arg2]

        self._memory[dest] = value1 + value2

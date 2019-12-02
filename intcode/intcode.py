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

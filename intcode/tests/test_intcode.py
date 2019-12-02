import unittest

import intcode

class Test_Program(unittest.TestCase):
    def test_pc_is_initially_zero(self):
        # Arrange
        program = intcode.Program([])

        # Act
        pc = program.pc

        # Assert
        self.assertEqual(pc, 0)

    def test_memory_is_copied(self):
        # Arrange
        initial_value = 42
        initial_memory = [initial_value]
        memory_offset = 0
        program = intcode.Program(initial_memory)

        # Act
        program.memory[memory_offset] = 0

        # Assert
        self.assertEqual(initial_memory[memory_offset], initial_value)

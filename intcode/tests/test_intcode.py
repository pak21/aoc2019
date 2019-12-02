import unittest

from parameterized import parameterized

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

    @parameterized.expand([
        ([1, 1, 2, 4, 0], [1, 1, 2, 4, 3]),
        ([1, 4, 5, 6, 7, 8, 0], [1, 4, 5, 6, 7, 8, 15]),
    ])
    def test_single_add_instruction(self, initial_memory, expected):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.memory, expected)
        self.assertEqual(program.pc, 4)
        self.assertFalse(terminated)

    @parameterized.expand([
        ([2, 1, 2, 4, 0], [2, 1, 2, 4, 2]),
        ([2, 4, 5, 6, 7, 8, 0], [2, 4, 5, 6, 7, 8, 56]),
    ])
    def test_single_multiply_instruction(self, initial_memory, expected):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.memory, expected)
        self.assertEqual(program.pc, 4)
        self.assertFalse(terminated)

    def test_terminate_instruction(self):
        # Arrange
        program = intcode.Program([99])

        # Act
        terminated = program.single_step()

        # Assert
        self.assertTrue(terminated)

    def test_unknown_opcode_throws_correct_exception(self):
        # Arrange
        program = intcode.Program([255])

        # Act / Assert
        with self.assertRaises(intcode.UnknownOpcodeException):
            program.single_step()

    @parameterized.expand([
        ([1, 0, 0, 3, 99], [1, 0, 0, 2, 99]),
        ([1, 0, 0, 3, 1, 1, 1, 3, 99], [1, 0, 0, 0, 1, 1, 1, 3, 99]),
    ])
    def test_run(self, initial_memory, expected):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        program.run()

        # Assert
        self.assertEqual(program.memory, expected)

class Test_Program_Day2(unittest.TestCase):
    """Integration tests from Advent of Code Day 2"""

    @parameterized.expand([
        ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ])
    def test_example(self, initial_memory, expected):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        program.run()

        # Assert
        self.assertEqual(program.memory, expected)

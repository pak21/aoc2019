import unittest

import itertools
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

    def test_outputs_starts_empty(self):
        # Arrange
        program = intcode.Program([])

        # Act
        outputs = program.outputs

        # Assert
        self.assertFalse(outputs) # Expect an empty list

    @parameterized.expand([
        ([1, 1, 2, 4, 0], [1, 1, 2, 4, 3]),
        ([1, 4, 5, 6, 7, 8, 0], [1, 4, 5, 6, 7, 8, 15]),
        ([101, 3, 3, 4, 0], [101, 3, 3, 4, 7]),
        ([1001, 0, 2, 4, 0], [1001, 0, 2, 4, 1003]),
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
        ([102, 3, 1, 3], [102, 3, 1, 9]),
        ([1002, 2, 4, 3], [1002, 2, 4, 16]),
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

    def test_single_input_instruction(self):
        # Arrange
        expected = 42
        program = intcode.Program([3, 2, 0], expected)

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.memory[2], expected)
        self.assertEqual(program.pc, 2)
        self.assertFalse(terminated)

    @parameterized.expand([
        ([4, 2, 42], 42),
        ([104, 2, 42], 2),
    ])
    def test_single_output_instruction(self, initial_memory, expected_output):
        # Arrange
        expected = 42
        program = intcode.Program(initial_memory)

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.pc, 2)
        self.assertEqual(program.outputs, [expected_output])
        self.assertFalse(terminated)

    @parameterized.expand([
        ([5, 0, 4, 0, 42], 42),
        ([105, 0, 4, 0, 42], 3),
        ([1005, 0, 4, 0, 42], 4),
    ])
    def test_single_jump_if_true_instruction(self, initial_memory, expected_pc):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.pc, expected_pc)
        self.assertFalse(terminated)

    @parameterized.expand([
        ([6, 0, 4, 0, 42], 3),
        ([106, 0, 4, 0, 42], 42),
        ([1006, 3, 4, 0, 42], 4),
    ])
    def test_single_jump_if_false_instruction(self, initial_memory, expected_pc):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.pc, expected_pc)
        self.assertFalse(terminated)

    @parameterized.expand([
        ([7, 6, 5, 4, 42, 1, -1], 1),
        ([7, 6, 5, 4, 42, 1, 1], 0),
        ([7, 6, 5, 4, 42, -1, 1], 0),
        ([107, 6, 5, 4, 42, 1, -1], 0),
        ([1007, 6, 5, 4, 42, 1, 4], 1),
    ])
    def test_single_less_than_instruction(self, initial_memory, expected):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.memory[4], expected)
        self.assertFalse(terminated)

    @parameterized.expand([
        ([8, 6, 5, 4, 42, 1, 1], 1),
        ([8, 6, 5, 4, 42, -1, 1], 0),
        ([8, 6, 5, 4, 42, 1, -1], 0),
        ([108, 6, 5, 4, 42, 1, 1], 0),
        ([1008, 6, 5, 4, 42, 1, 5], 1),
    ])
    def test_single_equals_instruction(self, initial_memory, expected):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.memory[4], expected)
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

class Test_Program_Day5(unittest.TestCase):
    """Integration tests from Advent of Code Day 5"""

    @parameterized.expand([
        ([3, 0, 4, 0, 99], [42]),
        ([1002, 4, 3, 4, 33], []),
        ([1101, 100, -1, 4, 0], []),
    ])
    def test_examples(self, initial_memory, expected_outputs):
        # Arrange
        program = intcode.Program(initial_memory, 42)

        # Act
        program.run()

        # Assert
        self.assertEqual(program.outputs, expected_outputs)

    @parameterized.expand(
        itertools.product(
            [[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [3, 3, 1108, -1, 8, 3, 4, 3, 99]], # Programs
            [7, 8, 9], # Input values
        )
    )
    def test_equals_8(self, initial_memory, input_value):
        # Arrange
        program = intcode.Program(initial_memory, input_value)
        expected = 1 if input_value == 8 else 0

        # Act
        program.run()

        # Assert
        self.assertEqual(program.outputs, [expected])

    @parameterized.expand(
        itertools.product(
            [[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [3, 3, 1107, -1, 8, 3, 4, 3, 99]], # Programs
            [7, 8, 9], # Input values
        )
    )
    def test_less_than_8(self, initial_memory, input_value):
        # Arrange
        program = intcode.Program(initial_memory, input_value)
        expected = 1 if input_value < 8 else 0

        # Act
        program.run()

        # Assert
        self.assertEqual(program.outputs, [expected])

    @parameterized.expand(
        itertools.product(
            [[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]], #Programs
            [-1, 0, 1], # Input values
        )
    )
    def test_jumps(self, initial_memory, input_value):
        # Arrange
        program = intcode.Program(initial_memory, input_value)
        expected = 1 if input_value != 0 else 0

        # Act
        program.run()

        # Assert
        self.assertEqual(program.outputs, [expected])

    @parameterized.expand([
        (7, 999),
        (8, 1000),
        (9, 1001),
    ])
    def test_final_example(self, input_value, expected):
        # Arrange
        program = intcode.Program(
            [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
            input_value
        )

        # Act
        program.run()

        # Assert
        self.assertEqual(program.outputs, [expected])

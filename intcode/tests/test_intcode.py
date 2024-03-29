import unittest

import itertools
from parameterized import parameterized

import intcode

def _generator():
    """Helper function for `test_input_generator`"""
    yield 100
    yield 101

class Test_Program(unittest.TestCase):
    def test_pc_is_initially_zero(self):
        # Arrange
        program = intcode.Program([])

        # Act
        pc = program.pc

        # Assert
        self.assertEqual(pc, 0)

    def test_relative_base_is_initially_zero(self):
        # Arrange
        program = intcode.Program([])

        # Act
        relative_base = program.relative_base

        # Assert
        self.assertEqual(relative_base, 0)

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

    def test_multiple_input_values(self):
        # Arrange
        expected1 = 42
        expected2 = 43
        program = intcode.Program([3, 4, 3, 5, 0, 0], input_values = [expected1, expected2])

        # Act
        program.single_step()
        program.single_step()

        # Assert
        self.assertEqual(program.pc, 4)
        self.assertEqual(program.memory[4], expected1)
        self.assertEqual(program.memory[5], expected2)

    def test_input_generator(self):
        # Arrange
        program = intcode.Program([3, 4, 3, 5, 0, 0], input_generator = _generator)

        # Act
        program.single_step()
        program.single_step()

        # Assert
        self.assertEqual(program.pc, 4)
        self.assertEqual(program.memory[4], 100)
        self.assertEqual(program.memory[5], 101)

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

    def test_output_with_relative_base(self):
        # Arrange
        expected = 42
        program = intcode.Program([109, 5, 204, -1, expected, 0])
        program.single_step() # Set relative base

        # Act
        program.single_step()

        # Assert
        self.assertEqual(program.outputs, [expected])

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

    def test_single_adjust_relative_base_instruction(self):
        # Arrange
        expected = 42
        program = intcode.Program([109, expected])

        # Act
        terminated = program.single_step()

        # Assert
        self.assertEqual(program.relative_base, expected)
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

    def test_unknown_addressing_mode_throws_correct_exception(self):
        # Arrange
        program = intcode.Program([304, 1])

        # Act / Assert
        with self.assertRaises(intcode.InvalidAddressingModeException):
            program.single_step()

    def test_immediate_mode_output_parameter_throws_correct_exception(self):
        # Arrange
        program = intcode.Program([11101, 1, 2, 3])

        # Act / Assert
        with self.assertRaises(intcode.InvalidAddressingModeException):
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

    def test_run_to_output(self):
        # Arrange
        program = intcode.Program([
            1101, 12, 34, 5, 104, 0, # Should be executed
            98 # Invalid opcode, should not be executed
        ])

        # Act
        program.run_to_output()

        # Assert
        self.assertEqual(program.outputs, [46])
        self.assertEqual(program.pc, 6)

    @parameterized.expand([
        ([109, 9, 1201, -2, 10, 8, 99, 5, 999], 15),
        ([109, 11, 2102, 5, -4, 8, 99, 7, 999], 35),
        ([109, 4, 21102, 11, 13, 4, 99, 999, 999], 143),
    ])
    def test_relative_addressing_mode(self, initial_memory, expected):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        program.run()

        # Assert
        self.assertEqual(program.memory[8], expected)

    def test_infinite_memory(self):
        # Arrange
        program = intcode.Program([4, 998, 1101, 2, 3, 999, 4, 999, 99])

        # Act
        program.run()

        # Assert
        self.assertEqual(program.outputs, [0, 5])

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

class Test_Program_Day9(unittest.TestCase):
    """Integration tests for Advent of Code Day 9."""

    def test_quine(self):
        # Arrange
        initial_memory = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        program = intcode.Program(initial_memory)

        # Act
        program.run()

        # Assert
        self.assertEqual(program.outputs, initial_memory)

    @parameterized.expand([
        ([1102, 34915192, 34915192, 7, 4, 7, 99, 0], 1219070632396864),
        ([104, 1125899906842624, 99], 1125899906842624),
    ])
    def test_big_numbers(self, initial_memory, expected):
        # Arrange
        program = intcode.Program(initial_memory)

        # Act
        program.run()

        # Assert
        self.assertEqual(program.outputs[0], expected)

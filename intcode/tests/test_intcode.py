import unittest

import intcode

class Test_Program(unittest.TestCase):
    def test_pc_is_initially_zero(self):
        # Arrange
        program = intcode.Program()

        # Act
        pc = program.pc

        # Assert
        self.assertEqual(pc, 0)

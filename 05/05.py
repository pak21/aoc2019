#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.join('..', 'intcode'))

import intcode

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

input_value = int(sys.argv[2])

program = intcode.Program(memory, input_value)
program.run()

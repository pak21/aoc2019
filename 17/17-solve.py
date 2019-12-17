#!/usr/bin/env python3

import os
import sys

import numpy as np

sys.path.append(os.path.join('..', 'intcode'))

import intcode

INSTRUCTIONS="""A,B,A,C,A,B,C,B,C,B
L,10,R,8,L,6,R,6
L,8,L,8,R,8
R,8,L,6,L,10,L,10
n
"""

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

memory[0] = 2

program = intcode.Program(memory, input_values=[ord(i) for i in INSTRUCTIONS])
program.run()
print(program.outputs[-1])

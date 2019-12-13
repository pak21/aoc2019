#!/usr/bin/env python3

import os
import sys

import numpy as np

sys.path.append(os.path.join('..', 'intcode'))

import intcode

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

# Part 1

program = intcode.Program(memory)
program.run()

screen = np.reshape(np.array(program.outputs), (-1, 3))
print('Number of blocks = {}'.format(np.sum(screen[:,2] == 2)))

# Part 2

memory[0] = 2
inputs = []
program2 = intcode.Program(memory, input_values=inputs)

ball = None
paddle = None

while True:
    before = len(program2.outputs)
    program2.run_to_output()
    if len(program2.outputs) == before:
        break
    program2.run_to_output()
    program2.run_to_output()

    x = program2.outputs.pop(0)
    y = program2.outputs.pop(0)
    tile_id = program2.outputs.pop(0)

    if x == -1:
        score = tile_id
    elif tile_id == 3:
        paddle = x
    elif tile_id == 4:
        ball = x

    if ball and paddle:
        if ball < paddle:
            inputs.append(-1)
            ball = None
            paddle = None
        elif ball > paddle:
            inputs.append(1)
            ball = None
            paddle = None
        else:
            inputs.append(0)
            ball = None

print('Final score = {}'.format(score))

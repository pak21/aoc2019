#!/usr/bin/env python3

import os
import random
import sys

sys.path.append(os.path.join('..', 'intcode'))

import intcode

def show_map(data, oxygen):
    min_x = min([t[0] for t in data.keys()])
    max_x = max([t[0] for t in data.keys()])
    min_y = min([t[1] for t in data.keys()])
    max_y = max([t[1] for t in data.keys()])

    dx = max_x - min_x + 1
    dy = max_y - min_y + 1

    print(dx, dy)

    squares = [([' '] * dx) for y in range(dy)]

    for k, v in data.items():
        x, y = k
        empty, dist = v 
        squares[y - min_y][x - min_x] = '.' if empty else '#'

    squares[-min_y][-min_x] = '!'

    if oxygen:
        squares[oxygen[1] - min_y][oxygen[0] - min_x] = '$'

    print('\n'.join([''.join(row) for row in squares]))

MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

inputs = []
program = intcode.Program(memory, input_values=inputs)

pos = (0, 0)
data = {
    (0, 0): (True, 0)
    }

random.seed(42)

n = 0
while True:
    direction = random.randrange(4) + 1
    step = MOVES[direction-1]
    new_pos = (pos[0] + step[0], pos[1] + step[1])

    if new_pos in data:
        next

    inputs.append(direction)
    program.run_to_output()

    result = program.outputs[-1]
    if result == 0:
        # Wall
        data[new_pos] = (False, None)
    else:
        if new_pos not in data:
            data[new_pos] = (True, data[pos][1] + 1)
        pos = new_pos

        if result == 2:
            # Oxygen
            print('Oxygen at {}'.format(new_pos))
            oxygen = new_pos
            break

show_map(data, oxygen)

print(data[oxygen])

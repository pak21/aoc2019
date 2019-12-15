#!/usr/bin/env python3

import os
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

    for k, empty in data.items():
        x, y = k
        squares[y - min_y][x - min_x] = '.' if empty else '#'

    squares[-min_y][-min_x] = '!'

    if oxygen:
        squares[oxygen[1] - min_y][oxygen[0] - min_x] = '$'

    print('\n'.join([''.join(row) for row in squares]))

MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
REVERSES = [1, 0, 3, 2]

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

inputs = []
program = intcode.Program(memory, input_values=inputs)

data = {
    (0, 0): True
    }

def do_recursive_move(data, pos, direction):
    step = MOVES[direction]
    new_pos = (pos[0] + step[0], pos[1] + step[1])

    if new_pos in data:
        return

    inputs.append(direction + 1)
    program.run_to_output()

    result = program.outputs.pop(0)
    if result == 0:
        # Wall
        data[new_pos] = False
    else:
        data[new_pos] = True
        for i in range(4):
            do_recursive_move(data, new_pos, i)

        inputs.append(REVERSES[direction] + 1)
        program.run_to_output()
        program.outputs.pop(0)

for i in range(4):
    do_recursive_move(data, (0, 0), i)

to_fill = [((18, 18), 0)]

while to_fill:
    current, time = to_fill.pop(0)
    for direction in range(4):
        step = MOVES[direction]
        new_pos = (current[0] + step[0], current[1] + step[1])

        if data[new_pos]:
            new_time = time + 1
            print('{} filled at time {}'.format(new_pos, new_time))
            to_fill.append((new_pos, new_time))
            data[new_pos] = False

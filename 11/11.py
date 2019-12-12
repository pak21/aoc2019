#!/usr/bin/env python3

import collections
import os
import sys

sys.path.append(os.path.join('..', 'intcode'))

import intcode

class Robot:
    def __init__(self):
        self.location = (0, 0)
        self.direction = 0

MOVES = [(0, -1), (1, 0), (0, 1), (-1, 0)]

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

inputs = []
program = intcode.Program(memory, input_values=inputs)

hull = collections.defaultdict(int)
painted = set()

def move(robot, paint, turn):
    hull[robot.location] = paint
    painted.add(robot.location)
    robot.direction = (robot.direction + (1 if turn else -1)) % 4
    robot.location = (robot.location[0] + MOVES[robot.direction][0], robot.location[1] + MOVES[robot.direction][1])

robot = Robot()

hull[robot.location] = 1

while True:
    inputs.append(hull[robot.location])
    program.run_to_output()
    if not len(program.outputs):
        break
    program.run_to_output()

    paint = program.outputs.pop(0)
    turn = program.outputs.pop(0)

    move(robot, paint, turn)

print('Painted {} squares'.format(len(painted)))

picture = [[' '] * 50 for y in range(6)]

for k, v in hull.items():
    if v:
        picture[k[1]][k[0]] = '#'

print('\n'.join([''.join(row) for row in picture]))

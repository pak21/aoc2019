#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.join('..', 'intcode'))

import intcode

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

# Part 1

memory[1] = 12
memory[2] = 2

program = intcode.Program(memory)
program.run()
print('Part 1 answer: {}'.format(program.memory[0]))

# Part 2

for noun in range(100):
    for verb in range(100):
        memory[1] = noun
        memory[2] = verb
        program = intcode.Program(memory)
        program.run()
        if program.memory[0] == 19690720:
            print('Part 2 answer: {} ({}, {})'.format(noun * 100 + verb, noun, verb))

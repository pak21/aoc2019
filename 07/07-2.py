#!/usr/bin/env python3

import itertools
import os
import sys

sys.path.append(os.path.join('..', 'intcode'))

import intcode

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

max_output = None
for phases in itertools.permutations([5, 6, 7, 8, 9]):
    inputs = [[x] for x in phases]
    programs = [intcode.Program(memory, input_values = inputs[i]) for i in range(5)]

    inputs[0].append(0)

    program_id = 0
    while True:
        program = programs[program_id]
        before = len(program.outputs)
        program.run_to_output()
        if len(program.outputs) == before:
            break
        next_program_id = (program_id + 1) % 5
        inputs[next_program_id].append(program.outputs[-1])
        program_id = next_program_id

    output = programs[4].outputs[-1]
    if max_output is None or output > max_output:
        print('Phases {} -> {}'.format(phases, output))
        max_output = output

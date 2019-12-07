#!/usr/bin/env python3

import itertools
import os
import sys

sys.path.append(os.path.join('..', 'intcode'))

import intcode

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

max_signal = None
for phases in itertools.permutations([0, 1, 2, 3, 4]):
    signal = 0
    for i in range(5):
        inputs = [phases[i], signal]
        program = intcode.Program(memory, input_values = inputs)
        program.run()
        signal = program.outputs[0]
    if max_signal is None or signal > max_signal:
        print('Phases {} produced signal {}'.format(phases, signal))
        max_signal = signal

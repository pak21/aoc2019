#!/usr/bin/env python3

import sys

import numpy as np

with open(sys.argv[1]) as f:
    input_seq = np.array([int(x) for x in f.readline().strip()] * 10000)

offset = int(''.join([str(x) for x in input_seq[:7]]))
relevant = input_seq[offset:]

for phase in range(100):
    next_signal = np.zeros(relevant.shape, dtype=np.int)
    next_signal[-1] = relevant[-1]
    for i in range(1, relevant.shape[0]):
        next_signal[-(i+1)] = (relevant[-(i+1)] + next_signal[-i]) % 10
    relevant = next_signal

print(''.join([str(x) for x in relevant[:8]]))

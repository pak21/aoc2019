#!/usr/bin/env python3

import sys

import numpy as np

def single_digit(input_seq, pattern):
    return abs(np.dot(input_seq, pattern)) % 10

def make_pattern(input_seq, base_pattern, position):
    pattern = np.repeat(base_pattern, position + 1)
    repeats_needed = (input_seq.shape[0] + pattern.shape[0]) // pattern.shape[0]
    repeated_pattern = np.tile(pattern, repeats_needed)[1:input_seq.shape[0]+1]
    return repeated_pattern

def doit(input_seq, base_pattern, i):
    pattern = make_pattern(input_seq, base_pattern, i)
    return single_digit(input_seq, pattern)

def do_phase(input_seq, base_pattern):
    next_signal = np.array([doit(input_seq, base_pattern, i) for i in range(input_seq.shape[0])])
    return next_signal

with open(sys.argv[1]) as f:
    input_seq = np.array([int(x) for x in f.readline().strip()])
print(input_seq.shape[0])

base_pattern = [0, 1, 0, -1]

for i in range(1):
    input_seq = do_phase(input_seq, base_pattern)

#!/usr/bin/env python3

import sys

import numpy as np

width = int(sys.argv[2])
height = int(sys.argv[3])

with open(sys.argv[1]) as f:
    digits = [int(x) for x in f.readline().strip()]

image = np.reshape(np.array(digits, dtype=np.uint8), (-1, height, width))

# Part 1

counts = [np.sum(image == i, axis=(1, 2)) for i in range(3)]
minzeros = np.argmin(counts[0])
print(counts[1][minzeros] * counts[2][minzeros])

# Part 2

pixel_values = np.apply_along_axis(lambda a: a[np.argmax(a != 2)], 0, image)
print('\n'.join([''.join(['#' if pixel else ' ' for pixel in row]) for row in pixel_values]))

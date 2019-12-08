#!/usr/bin/env python3

import sys

import numpy as np

width = int(sys.argv[2])
height = int(sys.argv[3])

with open(sys.argv[1]) as f:
    digits = [int(x) for x in f.readline().strip()]

image = np.reshape(digits, (-1, height, width))

# Part 1

counts = [np.sum(image == i, axis=(1, 2)) for i in range(3)]
minzeros = np.argmin(counts[0])
print(counts[1][minzeros] * counts[2][minzeros])

# Part 2

def firstmatching(image, x, y):
    return image[np.argmax(image[:,y,x] != 2),y,x]

for y in range(image.shape[1]):
    print(''.join([('#' if firstmatching(image, x, y) else ' ') for x in range(image.shape[2])]))

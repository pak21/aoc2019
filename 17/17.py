#!/usr/bin/env python3

import os
import sys

import numpy as np

sys.path.append(os.path.join('..', 'intcode'))

import intcode

TEST_SCAFFOLD = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""

def get_scaffold(test_mode):
    if test_mode:
        return TEST_SCAFFOLD
    else:
        with open(sys.argv[1]) as f:
            line = f.readline().strip()
            memory = [int(x) for x in line.split(',')]

        program = intcode.Program(memory)
        program.run()

        scaffold = [chr(x) for x in program.outputs]
        return (''.join(scaffold)).strip()

def parse_scaffold_string(s):
    return np.array([[x != '.' for x in row] for row in s.split('\n')])

def find_intersections(scaffold):
    intersections = []
    for index, c in np.ndenumerate(scaffold):
        y, x = index
        if not c or y == 0 or y == scaffold.shape[0] - 1 or x == 0 or x == scaffold.shape[1] - 1:
            continue
        if scaffold[y-1][x] and scaffold[y+1][x] and scaffold[y][x-1] and scaffold[y][x+1]:
            print('Intersection at {}'.format(index))
            intersections.append(index)

    return intersections


def main():
    test_mode = int(sys.argv[2])
    scaffold_string = get_scaffold(test_mode)
    scaffold = parse_scaffold_string(scaffold_string)
    intersections = find_intersections(scaffold)
    alignment = sum([i[0] * i[1] for i in intersections])
    print(alignment)

if __name__ == '__main__':
    main()

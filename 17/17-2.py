#!/usr/bin/env python3

import os
import sys

import numpy as np

sys.path.append(os.path.join('..', 'intcode'))

import intcode

TEST_SCAFFOLD = """#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......"""

MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]

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
    data = np.array([[x for x in row] for row in s.split('\n')])
    scaffold = data != '.'
    initial_position = [index for index, c in np.ndenumerate(data) if c == '^'][0]
    return scaffold, initial_position

def main():
    test_mode = int(sys.argv[2])
    scaffold_string = get_scaffold(test_mode)
    scaffold, pos = parse_scaffold_string(scaffold_string)
    direction = 0

    moves = []

    # Turn right if we started at the left edge and left if we started at the right edge
    # Works for the test data and my input, might not work for yours
    turn = 1 if pos[1] == 0 else -1

    direction = (direction + turn) % 4

    while True:
        length = 0
        while True:
            move = MOVES[direction]
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if new_pos[0] < 0 or new_pos[0] >= scaffold.shape[0] or new_pos[1] < 0 or new_pos[1] >= scaffold.shape[1] or not scaffold[new_pos]:
                break
            pos = new_pos
            length += 1

        moves.append((turn, length))

        # Work out if we should turn left or right
        valid_turns = []
        for turn in [-1, 1]:
            new_dir = (direction + turn) % 4
            new_move = MOVES[new_dir]
            new_pos = (pos[0] + new_move[0], pos[1] + new_move[1])
            if new_pos[0] >= 0 and new_pos[0] < scaffold.shape[0] and new_pos[1] >= 0 and new_pos[1] < scaffold.shape[1] and scaffold[new_pos]:
                valid_turns.append(turn)

        if not valid_turns:
            break
        elif len(valid_turns) > 1:
            print('valid_turns: {}??'.format(valid_turns))
            break

        turn = valid_turns[0]
        direction = (direction + turn) % 4

    for move in moves:
        print(move)

if __name__ == '__main__':
    main()

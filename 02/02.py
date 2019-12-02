#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

if True:
    memory[1] = 12
    memory[2] = 2

pc = 0

while True:
    opcode = memory[pc]
    if opcode == 99:
        break

    arg1 = memory[pc+1]
    arg2 = memory[pc+2]
    dest = memory[pc+3]

    value1 = memory[arg1]
    value2 = memory[arg2]
    if opcode == 1:
        result = value1 + value2
        print('Setting {} to {} + {} = {}'.format(dest, value1, value2, result))
        memory[dest] = result
    elif opcode == 2:
        result = value1 * value2
        print('Setting {} to {} * {} = {}'.format(dest, value1, value2, result))
        memory[dest] = result
    else:
        print('Unknown opcode {}'.format(opcode))
        sys.exit(1)

    pc += 4

print(memory)

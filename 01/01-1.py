#!/usr/bin/env python3

import sys

total = 0

with open(sys.argv[1]) as f:
    for l in f:
        mass = int(l)
        fuel = (mass // 3) - 2
        total += fuel
        print(mass, fuel, total)

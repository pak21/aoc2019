#!/usr/bin/env python3

import sys

total = 0

with open(sys.argv[1]) as f:
    for l in f:
        mass = int(l)
        linetotal = 0
        while True:
            fuel = (mass // 3) - 2
            print('  {} requires {}, total is now {}'.format(mass, fuel, linetotal))
            if fuel < 0:
                break
            linetotal += fuel
            mass = fuel
        total += linetotal
        print('Overall total now {}'.format(total))

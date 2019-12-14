#!/usr/bin/env python3

import collections
import sys

def parse(s):
    quantity_s, chemical = s.split(' ')
    return int(quantity_s), chemical

reactions = {}

with open(sys.argv[1]) as f:
    for line in f:
        inputs_text, output_text = line.strip().split(' => ')
        inputs = [parse(i) for i in inputs_text.split(', ')]
        output_quantity, output_chemical = parse(output_text)
        reactions[output_chemical] = (output_quantity, inputs)

def ore_needed(fuel):
    spare = collections.defaultdict(int)
    ore_used = 0

    needed = [(fuel, 'FUEL')]

    while needed:
        quantity_to_make, chemical_to_make = needed.pop(0)

        if spare[chemical_to_make]:
            if spare[chemical_to_make] > quantity_to_make:
                spare[chemical_to_make] -= quantity_to_make
                continue
            else:
                quantity_to_make -= spare[chemical_to_make]
                spare[chemical_to_make] = 0

        reaction_quantity, inputs = reactions[chemical_to_make]

        times_needed = (quantity_to_make + reaction_quantity - 1) // reaction_quantity
        units_being_made = times_needed * reaction_quantity

        for i in inputs:
            input_quantity_needed = times_needed * i[0]
            if i[1] == 'ORE':
                ore_used += input_quantity_needed
            else:
                needed.append((input_quantity_needed, i[1]))

        if units_being_made > quantity_to_make:
            spare[chemical_to_make] += units_being_made - quantity_to_make

    return ore_used

current = 1
while True:
    ore_used = ore_needed(current)
    if ore_used > 1000000000000:
        break
    current *= 2

high = current
low = current // 2

while True:
    next_value = (high + low) // 2
    if next_value == high or next_value == low:
        break
    ore_used = ore_needed(next_value)
    if ore_used > 1000000000000:
        high = next_value
    else:
        low = next_value

print(low)

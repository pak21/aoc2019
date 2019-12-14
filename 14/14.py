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

spare = collections.defaultdict(int)
ore_used = 0

needed = [(1, 'FUEL')]

while needed:
    quantity_to_make, chemical_to_make = needed.pop(0)
    print('Trying to make {} {}'.format(quantity_to_make, chemical_to_make))

    if spare[chemical_to_make]:
        if spare[chemical_to_make] > quantity_to_make:
            print('Have {} {} spare, using these to complete reaction'.format(spare[chemical_to_make], chemical_to_make))
            spare[chemical_to_make] -= quantity_to_make
            continue
        else:
            quantity_to_make -= spare[chemical_to_make]
            print('Have {} {} spare, using these, now need to make {}'.format(spare[chemical_to_make], chemical_to_make, quantity_to_make))
            spare[chemical_to_make] = 0

    reaction_quantity, inputs = reactions[chemical_to_make]
    print('Reaction makes {} units and needs {}'.format(reaction_quantity, inputs))

    times_needed = (quantity_to_make + reaction_quantity - 1) // reaction_quantity
    units_being_made = times_needed * reaction_quantity
    print('Need to run the reaction {} times, making {} units'.format(times_needed, units_being_made))

    for i in inputs:
        input_quantity_needed = times_needed * i[0]
        if i[1] == 'ORE':
            ore_used += input_quantity_needed
            print('Using {} ore, now used {} in total'.format(input_quantity_needed, ore_used))
        else:
            print('Need to make {} of {}'.format(input_quantity_needed, i[1]))
            needed.append((input_quantity_needed, i[1]))

    if units_being_made > quantity_to_make:
        spare[chemical_to_make] += units_being_made - quantity_to_make
        print('Spares are now {}'.format(spare))

    print('Now need to make {}'.format(needed))
    print()

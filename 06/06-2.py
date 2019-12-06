#!/usr/bin/env python3

import collections
import sys

def path_to_root(start, parents):
    path = [start]
    while path[0] in parents:
        path = [parents[path[0]]] + path
    return path

links = collections.defaultdict(list)
parents = {}
seen = set()

with open(sys.argv[1]) as f:
    for line in [l.strip() for l in f]:
        first, second = line.split(')')
        links[first].append(second)
        parents[second] = first
        seen.add(second)

you = path_to_root('YOU', parents)
santa = path_to_root('SAN', parents)

shared_length = 0
while you[shared_length] == santa[shared_length]:
    shared_length += 1

print(you)
print(santa)
print(shared_length)

print(len(you) + len(santa) - 2 * shared_length - 2)

#!/usr/bin/env python3

import collections
import sys

links = collections.defaultdict(list)
seen = set()

with open(sys.argv[1]) as f:
    for line in [l.strip() for l in f]:
        first, second = line.split(')')
        links[first].append(second)
        seen.add(second)

root_nodes = links.keys() - seen

if len(root_nodes) != 1:
    print('Invalid root nodes: {}'.format(root_nodes))

distances = {}
to_visit = [(list(root_nodes)[0], 0)]
while to_visit:
    current, distance = to_visit.pop(0)
    distances[current] = distance
    for next_node in links[current]:
        to_visit.append((next_node, distance + 1))

print(distances)
print(sum(distances.values()))

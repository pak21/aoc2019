#!/usr/bin/env python3

import re
import sys

def contains_repeat(s):
    return re.match(r'(.)\1', s)

def contains_repeat_len2(s):
    matches = [t[0] for t in re.findall(r'((.)\2+)', s)]
    len2 = [len(s) == 2 for s in matches]
    return any(len2)

def not_descending(s):
    foo = zip(s[:-1], s[1:])
    bar = [t[1] >= t[0] for t in foo]
    baz = all(bar)
    return baz

def isvalid(s):
    return contains_repeat_len2(s) and not_descending(s)

start, end = [int(x) for x in sys.argv[1].split('-')]

for i in range(start, end + 1):
    if isvalid(str(i)):
        print(i)

#!/usr/bin/env python3

import os
import sys
import random
from collections import defaultdict

import numpy as np
import re

src = open("input.txt", "r").readlines()

example = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]
max_cid = len(src)

part1 = 0

instances: dict[int, int] = defaultdict(int)

for row in src:
    row = row.replace("  ", " ")
    m = re.match(r"Card\s+(\d+):([\d\s]+)\|([\d\s]+)", row)
    cid = int(m.group(1))
    winning = set([int(n) for n in m.group(2).strip().split(" ")])
    mine = set([int(n) for n in m.group(3).strip().split(" ")])

    wins = winning.intersection(mine)

    instances[cid] += 1

    if wins:
        part1 += 2 ** (len(wins) - 1)

        for x in range(len(wins)):
            v = cid + 1 + x
            if v <= max_cid:
                instances[v] += instances[cid]

print("part1", part1)
print("part1", sum(instances.values()))

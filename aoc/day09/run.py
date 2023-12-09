#!/usr/bin/env python3

import numpy as np

src = open("input.txt", "r").readlines()

example = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".splitlines()

# src = example

src = [np.array([int(x) for x in r.strip().split()]) for r in src if r.strip()]

part1 = 0
part2 = 0

for i, seq in enumerate(src):
    sub_sequences = [seq]

    while True:
        sub_sequences.append(np.diff(sub_sequences[-1]))
        if len(np.unique(sub_sequences[-1])) == 1:
            break

    for sseq in sub_sequences:
        part1 += sseq[-1]

    pn = 0
    for sseq in reversed(sub_sequences):
        pn = sseq[0] - pn

    part2 += pn

print("part1:", part1)
print("part2:", part2)

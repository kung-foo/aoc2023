#!/usr/bin/env python3

import os
import sys
import random
from collections import OrderedDict

import numpy as np

src = open("input.txt", "r").read()

example = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

# src = example

src = src.strip().split(",")


def hash(s: str) -> int:
    acc = 0
    for c in s:
        acc += ord(c)
        acc *= 17
        acc %= 256
    return acc


print("part1:", sum(map(hash, src)))

boxes = []
for _ in range(256):
    boxes.append({})

for p in src:
    if p[-1] == "-":
        label = p[0:-1]
        pos = hash(label)
        if label in boxes[pos]:
            del boxes[pos][label]

    else:
        label, focal = p.split("=")
        boxes[hash(label)][label] = int(focal)

part2 = 0
for i, box in enumerate(boxes):
    for j, (_, focal) in enumerate(box.items()):
        part2 += (i + 1) * (j + 1) * focal

print("part2:", part2)

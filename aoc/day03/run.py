#!/usr/bin/env python3

import os
import sys
import random
from typing import Iterator

import numpy as np

src = open("input.txt", "r").readlines()

example = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]


def load(s) -> np.ndarray:
    return np.stack([np.array(list(l)) for l in s])


schematic = load(src)

gears: set[tuple[int, int]] = set()
any_symbol: set = set()
parts: list = []

dim_x = schematic.shape[1]
dim_y = schematic.shape[0]


def neighbors(x, y) -> Iterator[tuple[int, int]]:
    for d in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
        yield d[0] + x, d[1] + y


for y in range(dim_x):
    x = 0
    while x < dim_x:
        p = schematic[y][x]
        pp = ""
        points = set()

        while True:
            p = schematic[y][x]
            if not p.isdigit():
                break

            points.update(neighbors(x, y))

            pp += p
            x += 1
            if x == dim_x:
                break

        if pp:
            parts.append(
                {
                    "id": int(pp),
                    "points": points,
                }
            )

        if p != "." and not p.isdigit():
            any_symbol.add((x, y))
            if p == "*":
                gears.add((x, y))

        x += 1


has_match = []

for pdef in parts:
    for pp in pdef["points"]:
        if pp in any_symbol:
            has_match.append(pdef["id"])
            break

print("part1:", np.sum(has_match))

gear_adj: dict[tuple[int, int], list[int]] = {}

for gear in gears:
    for pdef in parts:
        if gear in pdef["points"]:
            if gear not in gear_adj:
                gear_adj[gear] = []
            gear_adj[gear].append(pdef["id"])

part2 = 0

for adj in gear_adj.values():
    if len(adj) == 2:
        part2 += adj[0] * adj[1]

print("part2:", part2)

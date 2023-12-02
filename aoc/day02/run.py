#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").readlines()

example = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

games = {}

for g in src:
    gid, sets = g.split(": ")
    gid = int(gid.replace("Game ", ""))

    games[gid] = []

    for s in sets.split("; "):
        n = {}
        for c in s.split(", "):
            c = c.split(" ")
            n[c[1]] = int(c[0])
        games[gid].append(n)

p1 = 0
p2 = 0

for gid, game in games.items():
    ok = True
    mr, mg, mb = 0, 0, 0

    for s in game:
        r = s.get("red", 0)
        g = s.get("green", 0)
        b = s.get("blue", 0)

        mr = max(mr, r)
        mg = max(mg, g)
        mb = max(mb, b)

        if r > 12 or g > 13 or b > 14:
            ok = False

    if ok:
        p1 += gid

    p2 += mr * mg * mb

print("part1:", p1)
print("part1:", p2)

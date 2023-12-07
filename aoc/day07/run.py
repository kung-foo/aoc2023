#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
from collections import Counter

src = open("input.txt", "r").readlines()

example = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".splitlines()

# example = """
# QJJQ2 1
# JKKK2 2
# """.splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

JOKER = "b"

m = {
    "T": "a",
    "J": JOKER,
    "Q": "c",
    "K": "d",
    "A": "e",
}

hands = []

"""
f: 5 of a kind
e: 4 of a kind
d: full house
c: 3 of a kind
b: two pair
a: one pair
9: high card
"""


def hand_type(h: str) -> str:
    c = Counter(h)
    b = c.most_common(1)[0][1]  # count of most common card
    if len(c) == 1:
        return "f"
    if len(c) == 2:
        if b == 4:
            return "e"
        return "d"
    if len(c) == 3:
        if b == 3:
            return "c"
        return "b"
    if len(c) == 4:
        return "a"
    if len(c) == 5:
        return "9"


def with_joker(h: str) -> str:
    if JOKER not in h:
        return hand_type(h) + h

    best = h.replace(JOKER, "1")
    best = hand_type(best) + best

    for c in "23456789acde":
        check = h.replace(JOKER, c)
        check = hand_type(check) + check
        if check >= best:
            best = check

    assert JOKER not in best
    assert "1" not in best

    return best


for i, h in enumerate(src):
    h, s = h.split()
    orig = h

    for k, v in m.items():
        h = h.replace(k, v)

    wj = with_joker(h)
    hands.append(
        [
            hand_type(h) + h,
            int(s),
            orig,
            wj,
            i,  # original order
            h.replace(JOKER, "1"),  # downgraded joker
        ]
    )


part1 = 0
# tie goes to original order
for i, h in enumerate(sorted(hands, key=lambda h: (h[0], h[4]))):
    part1 += (i + 1) * h[1]

print("part1:", part1)
assert part1 == 6440 or part1 == 251287184


part2 = 0
# tie goes to original hand with downgraded joker
for i, h in enumerate(sorted(hands, key=lambda h: (h[3][0], h[5]))):
    part2 += (i + 1) * h[1]

assert part2 == 5905 or part2 == 250757288

print("part2:", part2)

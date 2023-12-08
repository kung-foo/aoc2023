#!/usr/bin/env python3
import itertools
from typing import Callable
import numpy as np
import re
from dataclasses import dataclass

src = open("input.txt", "r").readlines()

example = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".splitlines()

# src = example


@dataclass
class Node:
    name: str
    l: str
    r: str


src = [r.strip() for r in src if r.strip()]
inst = src.pop(0)
nodes: dict[str, Node] = {}

for line in src:
    (nid, l, r) = filter(None, re.split("[=, ()]", line))
    nodes[nid] = Node(name=nid, l=l, r=r)


def find(f: str, stop_fn: Callable[[str], bool]) -> tuple[str, int]:
    node = nodes[f]

    for c, d in enumerate(itertools.cycle(inst)):
        node = nodes[node.l] if d == "L" else nodes[node.r]

        if stop_fn(node.name):
            return node.name, c + 1


print("part1:", find("AAA", lambda name: name == "ZZZ")[1])

distances = []

for nid, node in nodes.items():
    if nid.endswith("A"):
        distances.append(find(nid, lambda name: name[2] == "Z")[1])

print("part2:", np.lcm.reduce(distances))

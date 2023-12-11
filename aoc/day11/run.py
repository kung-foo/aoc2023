#!/usr/bin/env python3

import itertools
import numpy as np

src = open("input.txt", "r").readlines()

example = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]


def load(s) -> np.ndarray:
    return np.stack([np.array(list(l)) for l in s])


galaxy_map = load(src)

assert galaxy_map.shape[0] == galaxy_map.shape[1]

dim = galaxy_map.shape[0]

fill_value = "x"

# columns

to_insert = []
for x in range(dim):
    if len(np.where(galaxy_map[:, x] == "#")[0]) == 0:
        to_insert.insert(0, x)


for c in to_insert:
    galaxy_map = np.insert(galaxy_map, c, np.full(dim, fill_value), axis=1)

# rows

to_insert = []
for y in range(dim):
    if len(np.where(galaxy_map[y] == "#")[0]) == 0:
        to_insert.insert(0, y)


for c in to_insert:
    galaxy_map = np.insert(
        galaxy_map, c, np.full(galaxy_map.shape[1], fill_value), axis=0
    )

galaxies = list(zip(*np.where(galaxy_map == "#")))


# new numeric array with "distances". default is 1
nmap = np.full(galaxy_map.shape, 1)
nmap = np.where(galaxy_map == fill_value, 1_000_000 - 1, nmap)  # minus one?!


def expanded_distance(g1, g2, is_part2: bool = False):
    row_range = sorted([g1[1], g2[1]])
    row = nmap[g1[0]][row_range[0] : row_range[1]]

    col_range = sorted([g1[0], g2[0]])
    col = nmap[:, g1[1]][col_range[0] : col_range[1]]

    if not is_part2:
        return len(row) + len(col)

    return col.sum() + row.sum()


part1 = 0
part2 = 0

for g1, g2 in itertools.combinations(galaxies, 2):
    part1 += expanded_distance(g1, g2, False)
    part2 += expanded_distance(g1, g2, True)


print("part1:", part1)
print("part2:", part2)

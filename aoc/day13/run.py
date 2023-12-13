#!/usr/bin/env python3

import numpy as np

src = open("input.txt", "r").read().split("\n\n")

example = """
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
""".split(
    "\n\n"
)

# src = example


def load(s) -> np.ndarray:
    return np.stack([np.array(list(l)) for l in s])


part1 = 0
part2 = 0

for i, v in enumerate(src):
    valley = load(filter(None, map(str.strip, v.split("\n"))))

    for axis in (0, 1):
        for c in range(1, valley.shape[axis]):
            v1, v2 = np.split(valley, [c], axis=axis)
            m = min(v1.shape[axis], v2.shape[axis])

            v1 = np.flip(v1, axis=axis)

            if axis == 0:
                v1 = v1[0:m, :]  # stupid np.resize not actually resizing...
                v2 = v2[0:m, :]
            else:
                v1 = v1[:, 0:m]
                v2 = v2[:, 0:m]

            if np.all(v1 == v2):
                if axis == 0:
                    part1 += 100 * c
                else:
                    part1 += c

            elif (np.prod(v1.shape) - 1) == np.count_nonzero(v1 == v2):
                if axis == 0:
                    part2 += 100 * c
                else:
                    part2 += c

print("part1:", part1)
print("part2:", part2)

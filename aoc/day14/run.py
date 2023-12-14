#!/usr/bin/env python3
import typing
import xxhash
import sys
import numpy as np

src = open("input.txt", "r").readlines()

example = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".splitlines()

after1 = """
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]
after1 = [r.strip() for r in after1 if r.strip()]


def load(s: list[str]) -> np.ndarray:
    return np.stack([np.array(list(ln)) for ln in s])


platform = load(src)

assert platform.shape[0] == platform.shape[0]

dim = platform.shape[0]


def look(pos: tuple[int, int], d: str) -> np.ndarray[str]:
    # moar indexing!
    match d:
        case "N":
            return platform[:, pos[0]][0 : pos[1]]
        case "S":
            return platform[:, pos[0]][pos[1] + 1 :]
        case "W":
            return platform[pos[1]][0 : pos[0]]
        case "E":
            return platform[pos[1]][pos[0] + 1 :]


def shift_by(view: list[str], d: str) -> int:
    s = 0
    # view is 1d array, but we need to read from the "correct" end
    index = -1 if d in "NW" else 0
    while view and (c := view.pop(index)) and c == ".":
        s += 1
    return s


def points(d: str = "N") -> typing.Iterator[tuple[int, int]]:
    match d:
        case "N":
            for y in range(dim):
                for x in range(dim):
                    yield x, y
        case "S":
            for y in range(dim - 1, -1, -1):
                for x in range(dim):
                    yield x, y
        case "W":
            for x in range(dim):
                for y in range(dim):
                    yield x, y
        case "E":
            for x in range(dim - 1, -1, -1):
                for y in range(dim):
                    yield x, y


def calc_load() -> int:
    load = 0

    for x, y in points():
        c = platform[y][x]
        if c == "O":
            load += dim - y

    return load


cycles = 1_000_000_000
look_up = {}
first_match = 0

for cycle in range(cycles):
    for d in "NWSE":
        for x, y in points(d):
            if platform[y][x] == "O":
                view = list(look((x, y), d))

                if (shift := shift_by(view, d)) and shift == 0:
                    continue

                platform[y][x] = "."

                match d:
                    case "N":
                        platform[y - shift][x] = "O"
                    case "S":
                        platform[y + shift][x] = "O"
                    case "E":
                        platform[y][x + shift] = "O"
                    case "W":
                        platform[y][x - shift] = "O"

        if cycle == 0 and d == "N":
            print("part1:", calc_load())

    hash = xxhash.xxh64(platform.tobytes()).hexdigest()

    if hash in look_up:
        prev = look_up[hash]
        cycle_len = cycle - prev["cycle"]

        if first_match == 0:
            first_match = cycle - cycle_len

        # this is.... not clear...
        if (cycles - first_match) % cycle_len == (cycle - first_match) % cycle_len + 1:
            print("part2:", prev["load"])
            sys.exit()
    else:
        look_up[hash] = {
            "cycle": cycle,
            "load": calc_load(),
        }

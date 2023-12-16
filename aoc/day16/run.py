#!/usr/bin/env python3

from copy import copy
from dataclasses import dataclass
import numpy as np

src = open("input.txt", "r").readlines()

example = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]


def load(s: list[str]) -> np.ndarray:
    return np.stack([np.array(list(ln)) for ln in s])


cave = load(src)


@dataclass(unsafe_hash=True)
class StepVector:
    x: int
    y: int
    d: str


def step(pos: StepVector) -> tuple[bool, StepVector]:
    next_step = copy(pos)

    match pos.d:
        case "r":
            next_step.x += 1
        case "l":
            next_step.x -= 1
        case "u":
            next_step.y -= 1
        case "d":
            next_step.y += 1

    is_wall = not (
        0 <= next_step.x < cave.shape[1] and 0 <= next_step.y < cave.shape[0]
    )

    return is_wall, next_step


class StandbyIonControl:
    energized: np.ndarray
    visited: set[StepVector]
    beams: list[StepVector]

    def __init__(self):
        self.energized = np.zeros(cave.shape)
        self.visited = set()
        self.beams = []

    def pew_pew(self, start: StepVector):
        pos = start
        val = str(cave[pos.y][pos.x])

        while True:
            if pos in self.visited:
                break

            self.visited.add(pos)
            self.energized[pos.y][pos.x] = True

            match pos.d + val:
                case "r|" | "l|":
                    pos.d = "d"
                    self.beams.append(StepVector(x=pos.x, y=pos.y, d="u"))

                case "u-" | "d-":
                    pos.d = "l"
                    self.beams.append(StepVector(x=pos.x, y=pos.y, d="r"))

                case "d\\":
                    pos.d = "r"
                case "u\\":
                    pos.d = "l"
                case "r\\":
                    pos.d = "d"
                case "l\\":
                    pos.d = "u"

                case "d/":
                    pos.d = "l"
                case "u/":
                    pos.d = "r"
                case "r/":
                    pos.d = "u"
                case "l/":
                    pos.d = "d"

            wall, pos = step(pos)

            if wall:
                break

            val = cave[pos.y][pos.x]

    def fire(self, start: StepVector) -> int:
        self.beams.append(start)

        while self.beams:
            self.pew_pew(self.beams.pop())

        return np.count_nonzero(self.energized)


part1 = StandbyIonControl().fire(StepVector(x=0, y=0, d="r"))

print("part1:", part1)

assert part1 in (46, 7788)

part2 = 0

for x in range(cave.shape[1]):
    part2 = max(
        part2,
        StandbyIonControl().fire(StepVector(x=x, y=0, d="d")),
        StandbyIonControl().fire(StepVector(x=x, y=cave.shape[0] - 1, d="u")),
    )

for y in range(cave.shape[0]):
    part2 = max(
        part2,
        StandbyIonControl().fire(StepVector(x=0, y=y, d="r")),
        StandbyIonControl().fire(StepVector(x=cave.shape[1] - 1, y=y, d="l")),
    )


print("part2:", part2)

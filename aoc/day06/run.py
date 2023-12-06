#!/usr/bin/env python3

src = open("input.txt", "r").readlines()

example = """
Time:      7  15   30
Distance:  9  40  200
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

races = list(zip(*[[int(x) for x in l.split()[1:]] for l in src]))


def solve(t: int, p: int) -> int:
    return (t - p) * p


part1 = 1
for race in races:
    c = 0
    for t in range(race[0]):
        d = solve(race[0], t)
        if d > race[1]:
            c += 1
    part1 *= c

print("part1", part1)

tt, td = [int("".join(l.split()[1:])) for l in src]
c = 0

for t in range(tt):
    d = solve(tt, t)
    if d > td:
        c += 1

print("part2:", c)

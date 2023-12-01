#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

puzzle_input = open("input.txt", "r").readlines()

example = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".splitlines()

# puzzle_input = example

puzzle_input = [r.strip() for r in puzzle_input if r.strip()]

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
rnumbers = [n[::-1] for n in numbers]


def find_first(s: str, num_set: list[str]):
    offset = 0

    while True:
        if s[offset:][0].isdigit():
            return int(s[offset:][0])

        for i, n in enumerate(num_set):
            if s[offset:].startswith(n):
                return i + 1
        offset += 1


part1 = 0
part2 = 0

for line in puzzle_input:
    digits = []

    for c in line:
        if c.isdigit():
            digits.append(int(c))

    part2 += 10 * find_first(line, numbers) + find_first(line[::-1], rnumbers)

    if len(digits) == 1:
        digits.append(digits[0])

    part1 += 10 * digits[0] + digits[-1]

print("part1:", part1)
print("part2:", part2)

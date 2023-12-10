#!/usr/bin/env python3

from print_color import print
import numpy as np
from skimage.morphology import flood_fill
import turtle
from PIL import Image

src = open("input.txt", "r").readlines()

example = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""".splitlines()

example = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".splitlines()

# src = example

replace = {
    ".": " ",
    "7": "┐",
    "F": "┌",
    "L": "└",
    "J": "┘",
    "S": "☺",
}


def replace_all(s: str) -> str:
    s = s.strip()
    for k, v in replace.items():
        s = s.replace(k, v)
    return s


src = [r.strip() for r in src if r.strip()]


def load(s) -> np.ndarray:
    return np.stack([np.array(list(l)) for l in s])


maze = load(src)

Point = tuple[int, int]


def possible(curr: Point) -> tuple[Point, Point]:
    x, y = curr
    match maze[y][x]:
        case "7":
            return (x - 1, y), (x, y + 1)
        case "F":
            return (x, y + 1), (x + 1, y)
        case "L":
            return (x, y - 1), (x + 1, y)
        case "J":
            return (x - 1, y), (x, y - 1)
        case "-":
            return (x - 1, y), (x + 1, y)
        case "|":
            return (x, y - 1), (x, y + 1)
    assert 0, f"wtf {x}, {y} {maze[y][x]}"


def next(curr: Point, prev: Point) -> Point:
    a, b = possible(curr)
    if a != prev:
        return a
    return b


y, x = np.where(maze == "S")

s = (x[0], y[0])

maze[s[1]][s[0]] = "F"  # TODO: be smarter
# maze[s[1]][s[0]] = "7"

pos = s
prev = possible(s)[0]
part1 = 0
path_points = {s}
path = [s]

while True:
    n = next(pos, prev)
    prev = pos
    pos = n
    part1 += 1
    path_points.add(pos)
    path.append(pos)
    if pos == s:
        break

print("part1:", int(part1 / 2))

for y in range(maze.shape[0]):
    for x in range(maze.shape[1]):
        if maze[y][x] == ".":
            print("*", color="yellow", end="")
        else:
            color = "green" if (x, y) in path_points else "red"
            print(replace_all(maze[y][x]), color=color, end="")
    print()


# turtle time!!! 🐢 🐢 🐢 🐢 🐀

turtle.penup()  # 🐢
turtle.screensize(4096, 4096)  # 🐢
scale = 4
maybe = True

for p in path:
    turtle.goto(p[0] * scale + scale / 2, -(p[1] * scale + scale / 2))  # 🐢
    if maybe:
        turtle.pendown()  # 🐢
        maybe = False

for y in range(maze.shape[0]):
    for x in range(maze.shape[1]):
        if (x, y) in path_points:
            continue
        turtle.penup()  # 🐢
        turtle.goto(x * scale + scale / 2, -(y * scale + scale / 2))  # 🐢
        turtle.pendown()  # 🐢
        turtle.dot(1, "red")  # 🐢

turtle.hideturtle()  #

cv = turtle.getcanvas()
cv.postscript(file="/tmp/turtle_output.eps", colormode="color")

img = Image.open("/tmp/turtle_output.eps")
img.save("turtle_output.png", "png")

turtle.exitonclick()

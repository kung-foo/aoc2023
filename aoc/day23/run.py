#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx

src = open("input.txt", "r").readlines()

example = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

dim = len(src)
tree = "#"
forest = nx.DiGraph()

start = (src[0].index("."), 0)
end = (src[dim - 1].index("."), dim - 1)


def valid_cell(p: tuple[int, int]) -> bool:
    return 0 <= p[0] < dim and 0 <= p[1] < dim and src[p[1]][p[0]] != tree


def valid_step(p1: tuple[int, int], p2: tuple[int, int], d: str) -> bool:
    c1 = src[p1[1]][p1[0]]
    c2 = src[p2[1]][p2[0]]

    if c1 == "." and c2 == ".":
        return True

    match d:
        case "n":
            if c2 == "v":
                return False
        case "s":
            if c2 == "^":  # never happens
                assert 0
        case "e":
            if c2 == "<":  # never happens
                assert 0
        case "w":
            if c2 == ">":
                return False

    return True


def neighbors(p: tuple[int, int]) -> list[tuple[int, int]]:
    n = (p[0], p[1] - 1)
    s = (p[0], p[1] + 1)
    e = (p[0] + 1, p[1])
    w = (p[0] - 1, p[1])

    if valid_cell(n) and valid_step(p, n, "n"):
        yield n

    if valid_cell(s) and valid_step(p, s, "s"):
        yield s

    if valid_cell(e) and valid_step(p, e, "e"):
        yield e

    if valid_cell(w) and valid_step(p, w, "w"):
        yield w


for y in range(dim):
    for x in range(dim):
        if src[y][x] == tree:
            continue

        for n in neighbors((x, y)):
            forest.add_edge((x, y), n, weight=1)

part1 = 0
for path in nx.all_simple_paths(forest, start, end):
    part1 = max(part1, len(path) - 1)

print("part1:", part1)


def plot(g: nx.Graph):
    pos = {(x, y): (y, -x) for x, y in g.nodes()}
    nx.draw_networkx(g, pos=pos)
    plt.show()


# plot(forest)

forest_summary = forest.copy().to_undirected()

# collapse every node with only two edges into a single edge
# pretty inefficient since i'm too lazy to handle concurrent graph modification in an iterator
while True:
    found_pair = False
    for node in forest_summary.nodes:
        if node == start:
            continue

        edges = forest_summary.edges(node, data=True)

        if len(edges) == 2:
            e1, e2 = edges
            forest_summary.remove_node(node)
            forest_summary.add_edge(
                e1[1], e2[1], weight=e1[2]["weight"] + e2[2]["weight"]
            )
            found_pair = True
            break

    if not found_pair:
        break

# plot(forest_summary)

part2 = 0
for path in nx.all_simple_paths(forest_summary, start, end):
    w = nx.path_weight(forest_summary, path, "weight")
    part2 = max(part2, w)

print("part2:", part2)

#!/usr/bin/env python3

import re
import networkx as nx
import matplotlib.pyplot as plt


def plot(g: nx.Graph):
    nx.draw_networkx(g, pos=nx.spring_layout(g))
    plt.show()


src = open("input.txt", "r").readlines()

example = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

apparatus = nx.Graph()

for line in src:
    components = re.findall(r"\w+", line)
    c1 = components[0]

    for cx in components[1:]:
        apparatus.add_edge(c1, cx)

apparatus.remove_edge("xzz", "kgl")
apparatus.remove_edge("vkd", "qfb")
apparatus.remove_edge("xxq", "hqq")

part1 = 1
for cc in nx.connected_components(apparatus):
    part1 *= len(cc)

print("part1:", part1)

# full screen, zoom in, find edge, repeat.
plot(apparatus)

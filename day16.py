# %%
import re
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202416)

print(data)

nn = data_to_numpy(data)
# nn = nn.T

size = len(data)


# shapedict = dict()
# for ii in range(size):
#     for jj in range(size):
#         shapedict[(ii, jj)] = nn[(ii, jj)]

grid = {i + j * 1j: c for i, r in enumerate(data) for j, c in enumerate(r.strip())}
startpos = [key for key, val in grid.items() if val == "S"][0]
endpos = [key for key, val in grid.items() if val == "E"][0]
directions = (1, -1, 0 + 1j, 0 - 1j)
rotations = (1, 0 + 1j, 0 - 1j)

# %%

best_positions = {
    pos: {dir: 1000000 for dir in directions} for pos in grid if grid[pos] != "#"
}


def step_forward(*, pos, heading, score):
    if grid[pos] == "E":
        if best_positions[pos][1] > score:
            best_positions[pos][1] = score
    else:
        for rot in rotations:
            dir = rot * heading
            possible_score = score + 1000 * (dir != heading)
            if grid[pos + dir] == "#":
                continue
            if best_positions[pos][dir] <= possible_score:
                continue
            best_positions[pos][dir] = possible_score
            step_forward(pos=pos + dir, heading=dir, score=possible_score + 1)


step_forward(pos=startpos, heading=1j, score=0)
print(best_positions[endpos][1])


# %%
best_positions = {
    pos: {dir: 1000000 for dir in directions} for pos in grid if grid[pos] != "#"
}


def step_forward(*, heading, score, path, bestpaths):
    pos = path[-1]
    if grid[pos] == "E":
        if best_positions[pos][1] == score:
            bestpaths.append(path.copy())
        elif best_positions[pos][1] > score:
            best_positions[pos][1] = score
            bestpaths = [path.copy()]
    else:
        for rot in rotations:
            dir = rot * heading
            possible_score = score + 1000 * (dir != heading)
            if grid[pos + dir] == "#":
                continue
            if best_positions[pos][dir] < possible_score:
                continue
            best_positions[pos][dir] = possible_score
            bestpaths = step_forward(
                heading=dir,
                score=possible_score + 1,
                path=path + [pos + dir],
                bestpaths=bestpaths,
            )
    return bestpaths


bestpaths = step_forward(heading=1j, score=0, path=[startpos], bestpaths=[])
print(len(set([bb for path in bestpaths for bb in path])))

# %%
from collections import defaultdict
from heapq import heappop, heappush

grid = {i + j * 1j: c for i, r in enumerate(data) for j, c in enumerate(r) if c != "#"}

(start,) = (p for p in grid if grid[p] in "S")

seen = []
best = 1e9
dist = defaultdict(lambda: 1e9)
todo = [(0, t := 0, start, 1j, [start])]

while todo:
    score, _, pos, dir, path = heappop(todo)

    if score > dist[pos, dir]:
        continue
    else:
        dist[pos, dir] = score

    if grid[pos] == "E" and score <= best:
        seen += path
        best = score

    for rot, pts in (1, 1), (1j, 1001), (-1j, 1001):
        new = pos + dir * rot
        if new in grid:
            heappush(todo, (score + pts, t := t + 1, new, dir * rot, path + [new]))

print(best, len(set(seen)))
# %%

# %%
import re
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202418)

print(data)

nn = data_to_numpy(data)
# nn = nn.T

# size = len(data)
size = 71


# shapedict = dict()
# for ii in range(size):
#     for jj in range(size):
#         shapedict[(ii, jj)] = nn[(ii, jj)]

# %%
size = 71
cutoff = 1024
grid = np.zeros((size, size), dtype=int)

for line in data[0:cutoff]:
    xx = int(line.split(",")[0])
    yy = int(line.split(",")[1])
    if xx == 0 and yy == 0:
        print(line)
    grid[xx, yy] = 1
newgrid = dict()
for ii in range(grid.shape[0]):
    for jj in range(grid.shape[1]):
        newgrid[ii + jj * 1j] = grid[ii, jj]
# grid = {i + j * 1j: c for i, r in enumerate(grid) for j, c in enumerate(r.strip())}
# %%
for line in grid:
    print("".join([str(x) for x in line.tolist()]))
# %%
startpos = 0 + 0j
endpos = size - 1 + size * 1j - 1j
directions = (1, -1, 0 + 1j, 0 - 1j)
visited = {ii: 435435435334 for ii in newgrid.keys()}
visited[0] = 0
spaces = [startpos]

moves = 0
while spaces:
    space = spaces.pop()
    moves = visited[space]
    for dir in directions:
        newspace = space + dir
        if visited.get(newspace, -1) > moves + 1 and newgrid.get(newspace, -1) == 0:
            visited[newspace] = moves + 1
            if newspace == endpos:
                print(moves + 1)
            else:
                spaces.append(newspace)


# %%
from heapq import heappop, heappush

cutoff_start = 1
size = 71
grid = np.zeros((size, size), dtype=int)
for line in data[0:cutoff_start]:
    xx = int(line.split(",")[0])
    yy = int(line.split(",")[1])
    grid[xx, yy] = 1
newgrid = dict()
for ii in range(grid.shape[0]):
    for jj in range(grid.shape[1]):
        newgrid[ii + jj * 1j] = grid[ii, jj]
startpos = 0 + 0j
endpos = size - 1 + size * 1j - 1j
directions = (1, -1, 0 + 1j, 0 - 1j)
for cutoff in range(cutoff_start, 100000):
    print(cutoff)

    line = data[cutoff]
    xx = int(line.split(",")[0])
    yy = int(line.split(",")[1])
    grid[xx, yy] = 1
    newgrid[xx + yy * 1j] = 1
    visited = {ii: 435435435334 for ii in newgrid.keys()}
    visited[0] = 0
    spaces = [(0, t := 0, startpos)]
    unsolved = True
    while spaces and unsolved:
        score, _, space = heappop(spaces)
        moves = visited[space]
        for dir in directions:
            newspace = space + dir
            if visited.get(newspace, -1) > moves + 1 and newgrid.get(newspace, -1) == 0:
                if newspace == endpos:
                    unsolved = False
                    break
                else:
                    visited[newspace] = moves + 1
                    heappush(spaces, (moves + 1, t := t + 1, newspace))
    if unsolved:
        print(cutoff, data[cutoff])
        break

# %%

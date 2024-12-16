# %%
import re
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202416)

# data = [
#     "###############",
#     "#.......#....E#",
#     "#.#.###.#.###.#",
#     "#.....#.#...#.#",
#     "#.###.#####.#.#",
#     "#.#.#.......#.#",
#     "#.#.#####.###.#",
#     "#...........#.#",
#     "###.#.#####.#.#",
#     "#...#.....#.#.#",
#     "#.#.#.###.#.#.#",
#     "#.....#...#.#.#",
#     "#.###.#.#.#.#.#",
#     "#S..#.....#...#",
#     "###############",
# ]

# data = [
#     "#################",
#     "#...#...#...#..E#",
#     "#.#.#.#.#.#.#.#.#",
#     "#.#.#.#...#...#.#",
#     "#.#.#.#.###.#.#.#",
#     "#...#.#.#.....#.#",
#     "#.#.#.#.#.#####.#",
#     "#.#...#.#.#.....#",
#     "#.#.#####.#.###.#",
#     "#.#.#.......#...#",
#     "#.#.###.#####.###",
#     "#.#.#...#.....#.#",
#     "#.#.#.#####.###.#",
#     "#.#.#.........#.#",
#     "#.#.#.#########.#",
#     "#S#.............#",
#     "#################",
# ]

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

# %%
startx, starty = [x.item() for x in np.where(nn == "S")]
endx, endy = [x.item() for x in np.where(nn == "E")]

directions = (1, -1, 0 + 1j, 0 - 1j)


# logic is this
# if it got to a square, it has a score for that square in each direction
# we should save those scores because we want the minimum
# we then wait until all paths are over
# %%

best_positions = {
    pos: {dir: 1000000 for dir in directions} for pos in grid if grid[pos] != "#"
}


def step_forward(pos, heading, score):
    # print(pos, heading, score)
    if grid[pos] == "E":
        if best_positions[pos][1] > score:
            best_positions[pos][1] = score
    else:
        for qq in directions:
            possible_score = score + 1000 * (qq != heading)
            if grid[pos + qq] == "#":
                continue
            if best_positions[pos][qq] <= possible_score:
                continue
            best_positions[pos][qq] = possible_score
            step_forward(pos + qq, qq, possible_score + 1)


step_forward(startpos, 1j, 0)
print(best_positions[endpos][1])


# %%
best_positions = {
    pos: {dir: 1000000 for dir in directions} for pos in grid if grid[pos] != "#"
}

doubled_positions = {
    pos: {dir: 1 for dir in directions} for pos in grid if grid[pos] != "#"
}


def step_forward(pos, heading, score, path, bestpaths):
    # print(pos, heading, score)
    if grid[pos] == "E":
        if best_positions[pos][1] == score:
            bestpaths.append(path.copy())
        elif best_positions[pos][1] > score:
            best_positions[pos][1] = score
            bestpaths = [path.copy()]
    else:
        for qq in directions:
            possible_score = score + 1000 * (qq != heading)
            if grid[pos + qq] == "#":
                continue
            if best_positions[pos][qq] < possible_score:
                continue
            if best_positions[pos][qq] == possible_score:
                doubled_positions[pos][qq] += 1
            best_positions[pos][qq] = possible_score
            bestpaths = step_forward(
                pos + qq, qq, possible_score + 1, path + [pos + qq], bestpaths
            )
    return bestpaths


bestpaths = step_forward(startpos, 1j, 0, [startpos], [])
print(best_positions[endpos][1])

# %%
print(len(set([bb for path in bestpaths for bb in path])))

# %%

# %%
import re
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202415)
print(data)


nn = data_to_numpy(data)
# nn = nn.T

size = len(data)

# shapedict = dict()
# for ii in range(size):
#     for jj in range(size):
#         shapedict[(ii, jj)] = nn[(ii, jj)]

# grid = {i + j * 1j: c for i, r in enumerate(data) for j, c in enumerate(r.strip())}

# %%
movemap = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

grid = [line for line in data if "#" in line]
ng = data_to_numpy(grid)

moves = "".join([line for line in data if "#" not in line and line != ""])
currenty = [iline for iline, line in enumerate(grid) if "@" in line][0]
currentx = grid[currenty].index("@")


def pushboxes(gg, xx, yy, mm):
    dx = movemap[mm][0]
    dy = movemap[mm][1]
    ix = xx + dx
    iy = yy + dy
    nboxes = 0
    movevalid = False
    while gg[ix, iy] != "#":
        if gg[ix, iy] == ".":
            movevalid = True
            break
        elif gg[ix, iy] == "O":
            nboxes += 1
        ix += dx
        iy += dy
    if movevalid:
        gg[xx, yy] = "."
        gg[xx + dx, yy + dy] = "@"
        for ii in range(nboxes):
            gg[xx + (ii + 2) * dx, yy + (ii + 2) * dy] = "O"
    return xx + movevalid * dx, yy + movevalid * dy, gg


for move in moves:
    print("m", currentx, currenty, move)
    print(ng)
    currentx, currenty, ng = pushboxes(ng, currentx, currenty, move)

score = 0
for ix in range(ng.shape[0]):
    for iy in range(ng.shape[1]):
        if ng[ix, iy] == "O":
            score += 100 * ix + iy
print(score)
# %%

nn = data_to_numpy(data)
# nn = nn.T

size = len(data)
movemap = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}  # x is from the top

grid = [line for line in data if "#" in line]
newgrid = []
for line in grid:
    newline = ""
    for char in line:
        if char == "#":
            newline += "##"
        elif char == "O":
            newline += "[]"
        elif char == ".":
            newline += ".."
        elif char == "@":
            newline += "@."
    newgrid.append(newline)
ng = data_to_numpy(newgrid)

moves = "".join([line for line in data if "#" not in line and line != ""])
currentx = [iline for iline, line in enumerate(newgrid) if "@" in line][0]
currenty = newgrid[currentx].index("@")


def pushbigboxes(gg, xx, yy, mm, debug=False):
    dx = movemap[mm][0]
    dy = movemap[mm][1]
    ix = xx + dx
    iy = yy + dy

    if dy != 0:  # easier
        nboxes = 0
        movevalid = False
        while gg[ix, iy] != "#":
            if gg[ix, iy] == ".":
                movevalid = True
                break
            elif gg[ix, iy] == "]":
                nboxes += 1
            ix += dx
            iy += dy
        if movevalid:
            gg[xx, yy] = "."
            gg[xx + dx, yy + dy] = "@"
            for ii in range(nboxes):
                if dy == 1:
                    gg[xx, yy + (2 * ii + 2) * dy] = "["
                    gg[xx, yy + (2 * ii + 2) * dy + 1] = "]"
                if dy == -1:
                    gg[xx, yy + (2 * ii + 2) * dy] = "]"
                    gg[xx, yy + (2 * ii + 2) * dy - 1] = "["

        return xx + movevalid * dx, yy + movevalid * dy, gg
    else:  # ugh

        if gg[ix, iy] == "#":
            return xx, yy, gg
        elif gg[ix, iy] == ".":
            gg[xx, yy] = "."
            gg[ix, iy] = "@"
            return ix, iy, gg

        allboxstack = []
        check_boxes = []
        movevalid = False
        unblocked = True

        if gg[ix, iy] == "[":
            check_boxes.append(
                (
                    (ix, iy),
                    (ix, iy + 1),
                )
            )
        elif gg[ix, iy] == "]":
            check_boxes.append(
                (
                    (ix, iy - 1),
                    (ix, iy),
                )
            )
        while unblocked and check_boxes:
            box = check_boxes.pop()
            if box in allboxstack:
                continue
            allboxstack.append(box)
            bx = box[0][0]
            by = box[0][1]
            by2 = box[1][1]
            if gg[bx + dx, by] == "#" or gg[bx + dx, by2] == "#":
                unblocked = False
                break
            if gg[bx + dx, by] == "[":
                check_boxes.append(
                    (
                        (bx + dx, by),
                        (bx + dx, by + 1),
                    )
                )
            if gg[bx + dx, by] == "]":
                check_boxes.append(
                    (
                        (bx + dx, by - 1),
                        (bx + dx, by),
                    )
                )
            if gg[bx + dx, by2] == "[":
                check_boxes.append(
                    (
                        (bx + dx, by2),
                        (bx + dx, by2 + 1),
                    )
                )
        if debug:
            print(allboxstack)
        if unblocked:
            oldgrid = gg.copy()
            for fullbox in allboxstack[::-1]:
                gg[fullbox[0][0], fullbox[0][1]] = "."
                gg[fullbox[1][0], fullbox[1][1]] = "."
            for fullbox in allboxstack[::-1]:
                gg[fullbox[0][0] + dx, fullbox[0][1]] = oldgrid[
                    fullbox[0][0], fullbox[0][1]
                ]
                gg[fullbox[1][0] + dx, fullbox[1][1]] = oldgrid[
                    fullbox[1][0], fullbox[1][1]
                ]
            gg[xx, yy] = "."
            gg[xx + dx, yy + dy] = "@"
            return xx + dx, yy + dy, gg
        else:
            return xx, yy, gg


lboxes = 0
rboxes = 0
for line in ng.tolist():
    lboxes += line.count("[")
    rboxes += line.count("[")
startpos = 6969  # nice? lol abject fail
# for line in ng.tolist():
#     print("".join(line))
for imove, move in enumerate(moves[0:]):
    currentx, currenty, ng = pushbigboxes(ng, currentx, currenty, move)
    # if imove > startpos:
    #     for line in ng.tolist():
    #         print("".join(line))
    # nlboxes = 0
    # nrboxes = 0
    # for line in ng.tolist():
    #     nlboxes += line.count("[")
    #     nrboxes += line.count("[")
    # if nlboxes != lboxes or nrboxes != rboxes:
    #     print("aaa", imove, nlboxes, nrboxes, lboxes, rboxes)
    #     break


score = 0
for ix in range(ng.shape[0]):
    for iy in range(ng.shape[1]):
        if ng[ix, iy] == "[":
            score += 100 * ix + iy
print(score)
# %%

# %%
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202413)
print(data)

# data = [
#     "Button A: X+94, Y+34",
#     "Button B: X+22, Y+67",
#     "Prize: X=8400, Y=5400",
#     "",
#     "Button A: X+26, Y+66",
#     "Button B: X+67, Y+21",
#     "Prize: X=12748, Y=12176",
#     "",
#     "Button A: X+17, Y+86",
#     "Button B: X+84, Y+37",
#     "Prize: X=7870, Y=6450",
#     "",
#     "Button A: X+69, Y+23",
#     "Button B: X+27, Y+71",
#     "Prize: X=18641, Y=10279",
# ]

nn = data_to_numpy(data)
# nn = nn.T

size = len(data)

# shapedict = dict()
# for ii in range(size):
#     for jj in range(size):
#         shapedict[(ii, jj)] = nn[(ii, jj)]

# grid = {i + j * 1j: c for i, r in enumerate(data) for j, c in enumerate(r.strip())}

# %%
apushes = []
bpushes = []
prizeloc = []
for iline, line in enumerate(data):
    if iline % 4 == 0:
        dx = int(line.split("X+")[1].split(", ")[0])
        dy = int(line.split("Y+")[1])
        apushes.append((dx, dy))
    if iline % 4 == 1:
        dx = int(line.split("X+")[1].split(", ")[0])
        dy = int(line.split("Y+")[1])
        bpushes.append((dx, dy))
    if iline % 4 == 2:
        xx = int(line.split("X=")[1].split(", ")[0])
        yy = int(line.split("Y=")[1])
        prizeloc.append((xx, yy))

# %%
tokens = 0
for ap, bp, pz in zip(apushes, bpushes, prizeloc):
    print(ap, bp, pz)
    minpush = 1001
    for pusha in range(101):
        for pushb in range(101):
            if (
                pz[0] == pusha * ap[0] + pushb * bp[0]
                and pz[1] == pusha * ap[1] + pushb * bp[1]
            ):
                minpush = min(minpush, pusha * 3 + pushb)
                print("mp", minpush)
    if minpush < 1001:
        print(ap, bp, pz, minpush)
        tokens += minpush
print(tokens)
# %%
offset = 10000000000000
tokens = 0
for ap, bp, pz in zip(apushes, bpushes, prizeloc):
    px = pz[0] + offset
    py = pz[1] + offset

    AA = (px * bp[1] - py * bp[0]) / (ap[0] * bp[1] - ap[1] * bp[0])
    BB = (px * ap[1] - py * ap[0]) / (bp[0] * ap[1] - bp[1] * ap[0])
    # print(ap, bp, pz, AA, BB)
    if int(AA) == AA and int(BB) == BB:
        tokens += AA * 3 + BB
print(int(tokens))

# %%

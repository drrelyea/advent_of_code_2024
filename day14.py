# %%
import re
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202414)
print(data)
sx = 101
sy = 103
T = 100

# data = [
#     "p=0,4 v=3,-3",
#     "p=6,3 v=-1,-3",
#     "p=10,3 v=-1,2",
#     "p=2,0 v=2,-1",
#     "p=0,0 v=1,3",
#     "p=3,0 v=-2,-2",
#     "p=7,6 v=-1,-3",
#     "p=3,0 v=-1,-2",
#     "p=9,3 v=2,3",
#     "p=7,3 v=-1,2",
#     "p=2,4 v=2,-3",
#     "p=9,5 v=-3,-3",
# ]
# sx = 11
# sy = 7

nn = data_to_numpy(data)
# nn = nn.T

size = len(data)

# shapedict = dict()
# for ii in range(size):
#     for jj in range(size):
#         shapedict[(ii, jj)] = nn[(ii, jj)]

# grid = {i + j * 1j: c for i, r in enumerate(data) for j, c in enumerate(r.strip())}

# %%
quads = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
for robot in data:
    # print(robot)
    rs, vs = robot.split("p=")[1].split(" v=")
    rx, ry = [int(x) for x in rs.split(",")]
    vx, vy = [int(x) for x in vs.split(",")]
    # print(rx, ry, vx, vy)
    xx, yy = (rx + vx * T) % sx, (ry + vy * T) % sy
    # print("last", xx, yy)
    xq = 2
    yq = 2
    if xx < sx // 2:
        xq = 0
    elif xx > sx // 2:
        xq = 1
    if yy < sy // 2:
        yq = 0
    elif yy > sy // 2:
        yq = 1
    if xq < 2 and yq < 2:
        quads[(xq, yq)] += 1

import numpy as np

print(np.prod(list(quads.values())))
# %%
TT = 10000
xdist = np.zeros((TT, size))
ydist = np.zeros((TT, size))
for ii in range(TT):
    print(ii)
    nn = np.zeros((sx, sy))
    for irobot, robot in enumerate(data):
        rx, ry, vx, vy = re.findall(r"-?\d+", robot)
        xx, yy = (rx + vx * ii) % sx, (ry + vy * ii) % sy
        nn[xx, yy] = 1
        xdist[ii, irobot] = xx
        ydist[ii, irobot] = yy
    if np.var(xdist[ii, :]) < 750 or np.var(ydist[ii, :]) < 750:
        for line in nn.tolist():
            print("".join(["." if xx == 0 else "0" for xx in line]))
        print(ii)
        aa = input()

# %%

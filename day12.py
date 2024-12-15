# %%
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202412)
print(data)

nn = data_to_numpy(data)
nn = nn.T

size = len(data)

shapedict = dict()
for ii in range(size):
    for jj in range(size):
        shapedict[(ii, jj)] = nn[(ii, jj)]
# %%
grid = {i + j * 1j: c for i, r in enumerate(data) for j, c in enumerate(r.strip())}
sets = {p: {p} for p in grid}


# %%


def get_all_fences(dd):
    """
    coordinates: 0 is x, 1 is y
    fence in the 0 position borders the left edge
    fence in the 1 position borders the top edge
    grid is one larger than the data
    """
    fencedict = dict()
    for ii in np.arange(size + 1):
        for jj in np.arange(size + 1):
            fencedict[(ii, jj)] = [0, 0]  # left, top
    for ii in np.arange(size + 1):
        for jj in np.arange(size + 1):
            if ii == 0 or ii == size:
                fencedict[(ii, jj)][0] = 1  # left
            if jj == 0 or jj == size:
                fencedict[(ii, jj)][1] = 1  # top
            if dd.get((ii - 1, jj), "\x01") != dd.get((ii, jj), "\x02"):
                fencedict[(ii, jj)][0] = 1
            if dd.get((ii, jj - 1), "\x01") != dd.get((ii, jj), "\x02"):
                fencedict[(ii, jj)][1] = 1
    return fencedict


def addpoints(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def expand_blob_around_point(pp, dd):
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    extra_points = []
    for direction in directions:
        newpoint = addpoints(pp, direction)
        if dd.get(newpoint, "\x01") == dd[pp]:
            extra_points.append(newpoint)
    return extra_points


def find_blob_containing_point(pp, dd):
    current_blob = [pp]
    untried_points = [pp]
    while len(untried_points) > 0:
        untried_point = untried_points.pop()
        newpoints = expand_blob_around_point(untried_point, dd)
        newpoints = [nn for nn in newpoints if nn not in current_blob]
        current_blob += newpoints
        untried_points += newpoints
    return current_blob


def get_number_of_fences_around_point(pp, fd):
    nfence = 0
    if fd.get(pp, [0, 0])[0] == 1:
        nfence += 1
    if fd.get(pp, [0, 0])[1] == 1:
        nfence += 1
    if fd.get(addpoints(pp, (1, 0)), [0, 0])[0] == 1:
        nfence += 1
    if fd.get(addpoints(pp, (0, 1)), [0, 0])[1] == 1:
        nfence += 1
    return nfence


# %%
fencedict = get_all_fences(shapedict)

allpoints = list()
for ii in range(size):
    for jj in range(size):
        allpoints.append((ii, jj))


total = 0
while len(allpoints) > 0:
    point = allpoints[0]
    # print("op", point)
    blob_points = find_blob_containing_point(point, shapedict)
    # print("bp", blob_points)
    area = len(blob_points)
    fences = 0
    for blobpoint in blob_points:
        pointfences = get_number_of_fences_around_point(blobpoint, fencedict)
        print("bpfps", blobpoint, pointfences)
        fences += pointfences
    print(area, fences, blob_points)
    total += area * fences
    for blobpoint in blob_points:
        allpoints.remove(blobpoint)
print(total)


# %%


def get_fences_around_point(pp, fencedict, blob_fence_dict):
    if fencedict.get(pp, [0, 0])[0] == 1:
        if pp in blob_fence_dict:
            blob_fence_dict[pp][0] = 1
        else:
            blob_fence_dict[pp] = [1, 0]
    if fencedict.get(pp, [0, 0])[1] == 1:
        if pp in blob_fence_dict:
            blob_fence_dict[pp][1] = 1
        else:
            blob_fence_dict[pp] = [0, 1]
    if fencedict.get(addpoints(pp, (1, 0)), [0, 0])[0] == 1:
        aa = addpoints(pp, (1, 0))
        if aa in blob_fence_dict:
            blob_fence_dict[aa][0] = 1
        else:
            blob_fence_dict[aa] = [1, 0]
    if fencedict.get(addpoints(pp, (0, 1)), [0, 0])[1] == 1:
        aa = addpoints(pp, (0, 1))
        if aa in blob_fence_dict:
            blob_fence_dict[aa][1] = 1
        else:
            blob_fence_dict[aa] = [0, 1]
    return blob_fence_dict


def get_num_sides(blob_fence_dict, blobpoints):
    # print("bfd", blob_fence_dict)
    num_sides = 0
    for axis in (
        0,
        1,
    ):  # 0 means I am sorting by x and thus going vertically, so look at [0] fences
        remaining_fence_points = [
            point for point, fences in blob_fence_dict.items() if fences[axis] == 1
        ]
        sorted_points = sorted(
            remaining_fence_points, key=lambda x: (x[axis], x[1 - axis])
        )
        num_sides += 1
        for sp, nsp in zip(sorted_points, sorted_points[1:]):
            if sp[axis] != nsp[axis] or sp[1 - axis] != nsp[1 - axis] - 1:
                num_sides += 1
            if (
                sp[axis] == nsp[axis]
                and sp[1 - axis] == nsp[1 - axis] - 1
                and (
                    (sp in blobpoints and nsp not in blobpoints)
                    or sp not in blobpoints
                    and nsp in blobpoints
                )
            ):
                num_sides += 1

    return num_sides


allpoints = list()
for ii in range(size):
    for jj in range(size):
        allpoints.append((ii, jj))

total = 0
while len(allpoints) > 0:
    point = allpoints[0]
    # print("op", point)
    blob_points = find_blob_containing_point(point, shapedict)
    # print("bp", blob_points)
    area = len(blob_points)
    blob_fences = dict()
    for blobpoint in blob_points:
        blob_fences = get_fences_around_point(blobpoint, fencedict, blob_fences)
    num_sides = get_num_sides(blob_fences, blob_points)
    # print(area, fences, blob_points)
    total += area * num_sides
    for blobpoint in blob_points:
        allpoints.remove(blobpoint)
print(total)

# %%

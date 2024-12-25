# %%
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202425)
print(data)

nn = data_to_numpy(data)
# nn = nn.T

size = len(data)
# size = 71


# shapedict = dict()
# for ii in range(size):
#     for jj in range(size):
#         shapedict[(ii, jj)] = nn[(ii, jj)]


# %%
new_thing = []
locks = []
keys = []
for line in [""] + data:
    if not line:
        if new_thing:
            if new_thing[0] == "#####":
                locks.append(new_thing)
            elif new_thing[-1] == "#####":
                keys.append(new_thing)
            else:
                print("AAAAAAAA", new_thing)
        new_thing = []
    if line:
        new_thing.append(line)
# %%
lock_heights = []
key_heights = []
for lock in locks:
    better_lock = list(zip(*lock))
    lock_heights.append([row.count("#") for row in better_lock])
for key in keys:
    better_key = list(zip(*key))
    key_heights.append([row.count("#") for row in better_key])

# %%
npairs = 0
for lock in lock_heights:
    for key in key_heights:
        heightsum = [lh + kh for lh, kh in zip(lock, key)]
        if all([hh <= 7 for hh in heightsum]):
            npairs += 1
print(npairs)

# %%

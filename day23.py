# %%
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202423)

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
connections = defaultdict(list)
for line in data:
    aa = line.split("-")[0]
    bb = line.split("-")[1]
    connections[aa].append(bb)
    connections[bb].append(aa)
# %%
triplets = set()
ttriplets = set()
for term, seconds in connections.items():
    for second in seconds:
        thirds = connections[second]
        for third in thirds:
            if third in seconds:
                triplets.add(tuple(sorted([term, second, third])))
                if (
                    term.startswith("t")
                    or second.startswith("t")
                    or third.startswith("t")
                ):
                    ttriplets.add(tuple(sorted([term, second, third])))

# %%
largesets = {3: triplets}
might_be_bigger = True
set_size = 3
while might_be_bigger:
    print(set_size)
    might_be_bigger = False
    next_bigger = set()
    for triplet in largesets[set_size]:
        for link in connections[triplet[0]]:
            if link not in triplet and all(
                link in connections[triplet_item] for triplet_item in triplet
            ):
                next_bigger.add(tuple(sorted(list(triplet) + [link])))
                might_be_bigger = True
                continue
    set_size += 1
    largesets[set_size] = next_bigger

print(",".join(list(largesets[13])[0]))


# %%

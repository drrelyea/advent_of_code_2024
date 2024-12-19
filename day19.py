# %%
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202419)

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
patterns = data[0].split(", ")
pdict = defaultdict(list)
for pattern in patterns:
    pdict[pattern[0]].append(pattern)

for letter in pdict:
    pdict[letter] = sorted(pdict[letter], key=lambda x: -1 * len(x))

# %%
sweaters = data[2:]
for sweater in sweaters:

    @cache
    def solve_sweater(sweater):
        if len(sweater) == 0:
            return True
        first_letter = sweater[0]
        possible_patterns = pdict[first_letter]
        for ppattern in possible_patterns:
            if len(ppattern) <= len(sweater) and sweater[0 : len(ppattern)] == ppattern:
                if solve_sweater(sweater[len(ppattern) :]):
                    return True
        return False


print(sum(map(solve_sweater, sweaters)))

# %%
for sweater in sweaters:

    @cache
    def solve_sweater(sweater):
        if len(sweater) == 0:
            return 1
        first_letter = sweater[0]
        possible_patterns = pdict[first_letter]
        score = 0
        for ppattern in possible_patterns:
            if len(ppattern) <= len(sweater) and sweater[0 : len(ppattern)] == ppattern:
                score += solve_sweater(sweater[len(ppattern) :])
        return score


print(sum(map(solve_sweater, sweaters)))

# %%

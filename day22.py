# %%
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202422)

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
def upshift(x):
    return x * 64


def upmix(x):
    return (upshift(x) ^ x) % 16777216


def downshift(x):
    return x // 32


def downmix(x):
    return (downshift(x) ^ x) % 16777216


def upshift2(x):
    return x * 2048


def upmix2(x):
    return (upshift2(x) ^ x) % 16777216


def evolve(x):
    x = upmix(x)
    x = downmix(x)
    x = upmix2(x)
    return x


def evolveN(x, N):
    for _ in range(N):
        x = evolve(x)
    return x


def get_price_sequence(x):
    price_sequence = [x % 10]
    for _ in range(1, 2001):
        x = evolve(x)
        price_sequence.append(x % 10)
    return price_sequence


def get_delta_prices(price_sequence):
    return [x - y for (x, y) in zip(price_sequence[1:], price_sequence)]


def get_sequence_to_price_map(price_sequence):
    delta_sequence = get_delta_prices(price_sequence)
    sequence_to_price_map = dict()
    for ii in range(1, 2001 - 4):
        sequence = tuple(delta_sequence[ii : ii + 4])
        if sequence not in sequence_to_price_map:
            sequence_to_price_map[sequence] = price_sequence[ii + 4]
    return sequence_to_price_map


# %%
sum([evolveN(int(num), 2000) for num in data])
# %%
overall_sequence_to_price_map = defaultdict(int)
for num in data:
    price_sequence = get_price_sequence(int(num))
    sequence_to_price_map_for_this_number = get_sequence_to_price_map(price_sequence)
    for sequence, value in sequence_to_price_map_for_this_number.items():
        overall_sequence_to_price_map[sequence] += value

print(max(overall_sequence_to_price_map.values()))
# %%

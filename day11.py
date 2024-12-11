# %%
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202410)
print(data)


# nn = data_to_numpy(data, output_type=int)
# %%
@cache
def blink(num):
    if num == 0:
        return [1]
    elif len(str(num)) % 2 == 0:
        ll = len(str(num))
        return [int(str(num)[0 : ll // 2]), int(str(num)[ll // 2 :])]
    else:
        return [num * 2024]


def get_updated_numdict(numlist):
    new_numdict = {ii: 0 for ii in range(11)}
    for num in numlist:
        if num < 10:
            new_numdict[num] += 1
        else:
            new_numdict[10] += 1
    return new_numdict


# %%
numlist = [1]
for ii in range(10):
    newlist = []
    for num in numlist:
        newlist += blink(num)
    numlist = newlist
    print(numlist)

print(get_updated_numdict(numlist))
# %%

# %%
numlist = [int(xx) for xx in data[0].split(" ")]
print(numlist)
# %%


numerical_cycles = {
    0: {1: get_updated_numdict([1])},
    1: {3: get_updated_numdict([0, 2, 2, 4])},
    2: {3: get_updated_numdict([0, 4, 4, 8])},
    3: {3: get_updated_numdict([0, 2, 6, 7])},
    4: {3: get_updated_numdict([0, 6, 8, 9])},
    5: {5: get_updated_numdict([0, 0, 2, 2, 4, 8, 8, 8])},
    6: {5: get_updated_numdict([2, 4, 4, 5, 5, 6, 7, 9])},
    7: {5: get_updated_numdict([0, 2, 2, 3, 6, 6, 7, 8])},
    8: {4: get_updated_numdict([8]), 5: get_updated_numdict([2, 2, 3, 6, 7, 7])},
    9: {5: get_updated_numdict([1, 3, 4, 6, 6, 8, 8, 9])},
    10: {1: get_updated_numdict([])},
}

# %%

number_of_numbers_at_each_cycle = {inum: get_updated_numdict([]) for inum in range(11)}
for inum in range(10):
    numlist = [inum]
    for icycle in range(1, 6):
        newlist = []
        for num in numlist:
            newlist += blink(num)
        numlist = newlist
        number_of_numbers_at_each_cycle[inum][icycle] = len(numlist)


# %%
# thenum = 9
# numlist = [thenum]

# numlist = [125, 17]
# numlist = [8]
max_num_iterations = 75

# currentlist = numlist.copy()
# for ii in range(max_num_iterations):
#     newlist = []
#     for num in currentlist:
#         newlist += blink(num)
#     currentlist = newlist
#     # currentlist = [num for num in newlist if num > 9]
#     # print(currentlist)

#     # print(get_updated_numdict(currentlist))
# print("c", len(currentlist))
# # print(get_updated_numdict(currentlist))


# numlist = [125, 17]


# max_num_iterations = 25
iterations = [get_updated_numdict([]) for _ in range(max_num_iterations + 1)]
runningtotal = 0
for num in numlist:
    iteration = 0
    currentlist = [num]
    while currentlist and iteration < max_num_iterations:
        newlist = []
        for newnum in currentlist:
            if len(str(newnum)) == 1:
                iterations[iteration][newnum] += 1
            else:
                newlist += blink(newnum)
        currentlist = newlist
        iteration += 1
    newlist = []
    for newnum in currentlist:
        if len(str(newnum)) == 1:
            iterations[max_num_iterations][newnum] += 1
        else:
            iterations[max_num_iterations][10] += 1


for iteration in range(max_num_iterations):
    for num, num_multiplier in iterations[iteration].items():
        if num_multiplier > 0:
            if num == 8:
                if iteration + 5 > max_num_iterations:
                    # print(iteration, num, num_multiplier)
                    iterations[max_num_iterations][10] += (
                        num_multiplier
                        * number_of_numbers_at_each_cycle[num][
                            max_num_iterations - iteration
                        ]
                    )
                else:
                    for cycle_length in numerical_cycles[num]:
                        for (
                            end_state_number,
                            end_state_number_multiplier,
                        ) in numerical_cycles[num][cycle_length].items():
                            iterations[iteration + cycle_length][end_state_number] += (
                                num_multiplier * end_state_number_multiplier
                            )
            else:
                for cycle_length in numerical_cycles[num]:
                    if iteration + cycle_length > max_num_iterations:
                        # print(iteration, num, num_multiplier)
                        iterations[max_num_iterations][10] += (
                            num_multiplier
                            * number_of_numbers_at_each_cycle[num][
                                max_num_iterations - iteration
                            ]
                        )
                    else:
                        for (
                            end_state_number,
                            end_state_number_multiplier,
                        ) in numerical_cycles[num][cycle_length].items():
                            iterations[iteration + cycle_length][end_state_number] += (
                                num_multiplier * end_state_number_multiplier
                            )

# print(iterations[max_num_iterations])

for num, mult in iterations[max_num_iterations].items():
    runningtotal += mult

print(runningtotal)
# %%
# REDDIT SOLUTION FOR THE ENDING
# I SHOULD CACHE THE COUNT, NOT THE LIST
# OOPS
from functools import cache
from math import floor, log10


@cache
def count(x, d=75):
    if d == 0:
        return 1
    if x == 0:
        return count(1, d - 1)

    l = floor(log10(x)) + 1
    if l % 2:
        return count(x * 2024, d - 1)

    return count(x // 10 ** (l // 2), d - 1) + count(x % 10 ** (l // 2), d - 1)


print(sum(map(count, numlist)))

# %%


@cache
def count(num, iteration):
    if iteration == max_num_iterations:
        return 1
    elif num == 0:
        return count(1, iteration + 1)
    elif len(str(num)) % 2 == 0:
        ll = len(str(num))
        return count(int(str(num)[0 : ll // 2]), iteration + 1) + count(
            int(str(num)[ll // 2 :]), iteration + 1
        )
    else:
        return count(num * 2024, iteration + 1)


print(sum(count(num, 0) for num in numlist))

# %%

# %%
import itertools
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache, partial

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202421)
print(data)

# %%
key_for_num_coord = {
    1: "0",
    2: "A",
    0 + 1j: "1",
    1 + 1j: "2",
    2 + 1j: "3",
    0 + 2j: "4",
    1 + 2j: "5",
    2 + 2j: "6",
    0 + 3j: "7",
    1 + 3j: "8",
    2 + 3j: "9",
}

num_coord_for_key = {v: k for k, v in key_for_num_coord.items()}

key_for_arrow_coord = {
    0: -1,
    1: -1j,
    2: +1,
    1 + 1j: 1j,
    2 + 1j: "A",
}

arrow_coord_for_key = {v: k for k, v in key_for_arrow_coord.items()}


@cache
def break_down_steps(step):
    step_list = []
    if step.real == 1:
        step_list.append(1)
    elif step.real == 2:
        step_list.append(1)
        step_list.append(1)
    elif step.real == -1:
        step_list.append(-1)
    elif step.real == -2:
        step_list.append(-1)
        step_list.append(-1)
    if step.imag == 1:
        step_list.append(1j)
    elif step.imag == 2:
        step_list.append(1j)
        step_list.append(1j)
    elif step.imag == 3:
        step_list.append(1j)
        step_list.append(1j)
        step_list.append(1j)
    elif step.imag == -1:
        step_list.append(-1j)
    elif step.imag == -2:
        step_list.append(-1j)
        step_list.append(-1j)
    elif step.imag == -3:
        step_list.append(-1j)
        step_list.append(-1j)
        step_list.append(-1j)
    return step_list


def readable(sequence):
    complex_to_ascii = {1: ">", -1: "<", 1j: "^", -1j: "v", "A": "A"}
    return ("".join([complex_to_ascii.get(step, step) for step in sequence])).split("A")


@cache
def is_acceptable_arrow_sequence(start_key, sequence):
    if sequence:
        if (
            start_key == "A"
            and len(sequence) > 1
            and sequence[0] == -1
            and sequence[1] == -1
        ):
            return False
        if start_key == 1j and sequence[0] == -1:
            return False
        if start_key == -1 and sequence[0] == 1j:
            return False
    return True


@cache
def is_acceptable_num_sequence(start_key, sequence):
    if sequence:
        if (
            start_key == "A"
            and len(sequence) > 1
            and sequence[0] == -1
            and sequence[1] == -1
        ):
            return False
        if start_key == "0" and sequence[0] == -1:
            return False
        if start_key == "1" and sequence[0] == -1j:
            return False
        if (
            start_key == "4"
            and len(sequence) > 1
            and sequence[0] == -1j
            and sequence[1] == -1j
        ):
            return False
        if (
            start_key == "7"
            and len(sequence) > 2
            and sequence[0] == -1j
            and sequence[1] == -1j
            and sequence[2] == -1j
        ):
            return False
    return True


@cache
def move_to_new_arrow_coord_with_k_robots_left(start_key, end_key, k):
    # print(">>>>>", start_key, end_key, k)
    if k == 0:
        raise ValueError("K is 0! what?")
    old_arrow_coord = arrow_coord_for_key[start_key]
    new_arrow_coord = arrow_coord_for_key[end_key]
    unsorted_sequence = break_down_steps(
        (new_arrow_coord - old_arrow_coord).real
    ) + break_down_steps((new_arrow_coord - old_arrow_coord).imag * 1j)
    unfiltered_possible_sequences = itertools.permutations(unsorted_sequence)
    all_possible_sequences = []
    for sequence in unfiltered_possible_sequences:
        sequence = list(sequence)
        if is_acceptable_arrow_sequence(start_key, sequence):
            all_possible_sequences.append(sequence)
    if k == 1:
        best_sequence = all_possible_sequences[0] + ["A"]
    else:
        best_sequence = []
        best_sequence_length = 1492423432
        for sequence in all_possible_sequences:
            actual_sequence = sequence + ["A"]
            upstream_robot_chain = []
            for ii in range(k - 1):
                move_function = move_to_new_arrow_coord_with_k_robots_left
                upstream_robot_chain.append(Machine(move_function, k - 1 - ii))
            code_sequence = []
            for number in actual_sequence:
                code_sequence += get_sequence(upstream_robot_chain, number)
            if len(code_sequence) < best_sequence_length:
                # print("BBBB", k, len(code_sequence), code_sequence)
                best_sequence = actual_sequence
                best_sequence_length = len(code_sequence)
    return best_sequence


@cache
def move_to_new_num_coord_with_k_robots_left(start_key, end_key, k):
    # print("WWWW", start_key, end_key, k)
    if k == 0:
        raise ValueError("K is 0! what?")
    old_num_coord = num_coord_for_key[start_key]
    new_num_coord = num_coord_for_key[end_key]
    unsorted_sequence = break_down_steps(
        (new_num_coord - old_num_coord).real
    ) + break_down_steps((new_num_coord - old_num_coord).imag * 1j)
    unfiltered_possible_sequences = itertools.permutations(unsorted_sequence)
    all_possible_sequences = []
    for sequence in unfiltered_possible_sequences:
        sequence = list(sequence)
        if is_acceptable_num_sequence(start_key, sequence):
            all_possible_sequences.append(sequence)
    if k == 1:
        best_sequence = all_possible_sequences[0] + ["A"]
    else:
        best_sequence = []
        best_sequence_length = 1492423432
        for sequence in all_possible_sequences:
            actual_sequence = sequence + ["A"]
            upstream_robot_chain = []
            for ii in range(k - 1):
                move_function = move_to_new_arrow_coord_with_k_robots_left
                upstream_robot_chain.append(Machine(move_function, k - 1 - ii))
            code_sequence = []
            for number in actual_sequence:
                code_sequence += get_sequence(upstream_robot_chain, number)
            if len(code_sequence) < best_sequence_length:
                # print("AAAA", k, len(code_sequence), code_sequence)
                best_sequence = actual_sequence
                best_sequence_length = len(code_sequence)
    return best_sequence


def get_sequence(machines, newkey):
    current_step_seq = [newkey]
    for machine in machines:
        new_step_seq = []
        # print("aa", machine, readable(current_step_seq))
        for step in current_step_seq:
            new_step_seq += machine.move(step)
        current_step_seq = new_step_seq
    # print("mm", machine, readable(current_step_seq))
    return current_step_seq


class Machine:
    def __init__(self, move_func, k):
        self.current_key = "A"
        self.move_func = move_func
        self.k = k

    def move(self, new_key):
        return_seq = self.move_func(self.current_key, new_key, self.k)
        self.current_key = new_key
        return return_seq


# %%
goobster = data[0:]
total = 0
num_machine = Machine(move_to_new_num_coord_with_k_robots_left, 3)
all_machines = [num_machine]
n_robots = 18
for ii in range(n_robots):
    all_machines.append(
        Machine(move_to_new_arrow_coord_with_k_robots_left, n_robots - ii)
    )

for code in goobster:
    print("NEW CODE RESET")
    codesum = 0
    codenum = int(code.split("A")[0])
    code_sequence = []
    for number in code:
        code_sequence += get_sequence(
            all_machines,
            number,
        )
        # print(
        #     "cc",
        #     len(code_sequence),
        #     codenum,
        #     readable(code_sequence),
        # )
    total += len(code_sequence) * codenum
print(total)

# %%
# %%
# %%
import os
from pathlib import Path
from time import perf_counter

timer_script_start = perf_counter()
DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)][::2]
UP, RIGHT, DOWN, LEFT = DIRECTIONS


def add(*ps):
    return tuple(map(sum, zip(*ps)))


def sub(p1, p2):
    return tuple(a - b for a, b in zip(p1, p2))


timer_parse_start = perf_counter()
############################## PARSER ##############################
num_pad_lines = """
789
456
123
.0A
""".strip().splitlines()
dir_pad_lines = """
.^A
<v>
""".strip().splitlines()
num_pad = {
    (i, j): c
    for i, line in enumerate(num_pad_lines)
    for j, c in enumerate(line)
    if c != "."
}
dir_pad = {
    (i, j): c
    for i, line in enumerate(dir_pad_lines)
    for j, c in enumerate(line)
    if c != "."
}
num_pad.update({v: k for k, v in num_pad.items()})
dir_pad.update({v: k for k, v in dir_pad.items()})


def manhattan_distance(a, b=(0, 0)):
    d = 0
    for j, k in zip(a, b):
        d += abs(j - k)
    return d


timer_parse_end = timer_part1_start = perf_counter()


# DLLA RUAA RA
# LUUA


# LAA DLA RRUA
# UULA
############################## PART 1 ##############################
def step(source, target, pad):
    ti, tj = pad[target]
    si, sj = pad[source]
    di = ti - si
    dj = tj - sj
    vert = "v" * di + "^" * -di
    horiz = ">" * dj + "<" * -dj
    if dj > 0 and (ti, sj) in pad:
        return vert + horiz + "A"
    if (si, tj) in pad:
        return horiz + vert + "A"
    if (ti, sj) in pad:
        return vert + horiz + "A"


def routes(path, pad):
    out = []
    start = "A"
    for end in path:
        out.append(step(start, end, pad))
        start = end
    return "".join(out)


num_routes = [routes(line, num_pad) for line in goobster]
rad_routes = [routes(route, dir_pad) for route in num_routes]
cold_routes = [routes(route, dir_pad) for route in rad_routes]
p1 = sum(
    len(route) * int(line.split("A")[0]) for route, line in zip(cold_routes, goobster)
)
print("Part 1:", p1)
timer_part1_end = timer_part2_start = perf_counter()
# %%

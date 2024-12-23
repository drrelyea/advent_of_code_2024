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


def readable_pairs(pairs):
    complex_to_ascii = {1: ">", -1: "<", 1j: "^", -1j: "v", "A": "A"}
    return ("".join([complex_to_ascii.get(pair[1], "moops") for pair in pairs])).split(
        "A"
    )


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


# %%
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


# %%
def calculate_next_robot(input_sequence, input_dict):
    actual_input_sequence = ["A"] + input_sequence
    output_sequence = []
    for first, second in zip(actual_input_sequence, actual_input_sequence[1:]):
        output_sequence += input_dict[(first, second)]
    return output_sequence


# %%
button_presses_for_start_and_end_keys = defaultdict(set)
for start_key in arrow_coord_for_key:
    for end_key in arrow_coord_for_key:
        start_pos = arrow_coord_for_key[start_key]
        end_pos = arrow_coord_for_key[end_key]
        unsorted_sequence = break_down_steps(
            (end_pos - start_pos).real
        ) + break_down_steps((end_pos - start_pos).imag * 1j)
        unfiltered_possible_sequences = itertools.permutations(unsorted_sequence)
        for sequence in unfiltered_possible_sequences:
            sequence = list(sequence)
            if is_acceptable_arrow_sequence(start_key, sequence):
                if (
                    start_key == "A"
                    and end_key == -1
                    and sequence == [-1, (-0 - 1j), -1]
                ):
                    continue
                if start_key == -1 and end_key == "A" and sequence == [1, 1j, 1]:
                    continue
                button_presses_for_start_and_end_keys[(start_key, end_key)].add(
                    tuple(sequence + ["A"])
                )
button_presses_for_start_and_end_keys

best_button_presses_for_start_and_end_keys = {
    k: list(list(v)[0]) for k, v in button_presses_for_start_and_end_keys.items()
}

bbb = best_button_presses_for_start_and_end_keys.copy()

max_seq_length = 54354354353534
for ii in range(2):
    for jj in range(2):
        for kk in range(2):
            for ll in range(2):
                bbb = best_button_presses_for_start_and_end_keys.copy()
                bbb[(-1j, "A")] = [bbb[(-1j, "A")][ii], bbb[(-1j, "A")][1 - ii], "A"]
                bbb[(1j, 1)] = [bbb[(1j, 1)][jj], bbb[(1j, 1)][1 - jj], "A"]
                bbb[(1, 1j)] = [bbb[(1, 1j)][kk], bbb[(1, 1j)][1 - kk], "A"]
                bbb[("A", -1j)] = [bbb[("A", -1j)][ll], bbb[("A", -1j)][1 - ll], "A"]

                total_sequence_length = 0
                for sequence in bbb.keys():
                    current_sequence = list(sequence)
                    for _ in range(8):
                        current_sequence = calculate_next_robot(current_sequence, bbb)
                    total_sequence_length += len(current_sequence)
                if total_sequence_length < max_seq_length:
                    max_seq_length = total_sequence_length
                    print(max_seq_length, ii, jj, kk, ll)


# %%
def sequence_to_pair_counter(input_sequence):
    output_dict = defaultdict(int)
    for first, second in zip(["A"] + input_sequence, input_sequence):
        output_dict[(first, second)] += 1
    return output_dict


def pairs_to_pair_counter(input_pairs):
    output_dict = defaultdict(int)
    for pair in input_pairs:
        output_dict[pair] += 1
    return output_dict


def get_counts_per_pair_for_input_sequence(input_sequence, nrobots=10):
    counts_per_pair = sequence_to_pair_counter(input_sequence)
    for _ in range(nrobots):
        counts_per_new_pair = defaultdict(int)
        for input_pair, val in counts_per_pair.items():
            for output_pair in input_button_pairs_to_list_of_output_pairs[input_pair]:
                counts_per_new_pair[output_pair] += val
        counts_per_pair = counts_per_new_pair
    return counts_per_pair


def get_output_length_for_input_sequence(input_sequence, nrobots=10):
    counts_per_pair = get_counts_per_pair_for_input_sequence(
        input_sequence, nrobots=nrobots
    )
    return sum(counts_per_pair.values())


def get_counts_per_pair_for_input_pairs(input_pairs, nrobots=10):
    counts_per_pair = pairs_to_pair_counter(input_pairs)
    for _ in range(nrobots):
        counts_per_new_pair = defaultdict(int)
        for input_pair, val in counts_per_pair.items():
            for output_pair in input_button_pairs_to_list_of_output_pairs[input_pair]:
                counts_per_new_pair[output_pair] += val
        counts_per_pair = counts_per_new_pair
    return counts_per_pair


def get_output_length_for_input_pairs(input_pairs, nrobots=10):
    counts_per_pair = get_counts_per_pair_for_input_pairs(input_pairs, nrobots=nrobots)
    return sum(counts_per_pair.values())


get_output_length_for_input_sequence([-1j, -1j, -1, -1, "A"], nrobots=25)


# %%
num_button_presses_for_start_and_end_keys = defaultdict(set)
for start_key in num_coord_for_key:
    for end_key in num_coord_for_key:
        start_pos = num_coord_for_key[start_key]
        end_pos = num_coord_for_key[end_key]
        unsorted_sequence = break_down_steps(
            (end_pos - start_pos).real
        ) + break_down_steps((end_pos - start_pos).imag * 1j)
        unfiltered_possible_sequences = itertools.permutations(unsorted_sequence)
        for sequence in unfiltered_possible_sequences:
            if start_key == "A" and end_key == "5":
                print(sequence)
            sequence = list(sequence)
            if is_acceptable_num_sequence(start_key, sequence):
                num_button_presses_for_start_and_end_keys[(start_key, end_key)].add(
                    tuple(sequence + ["A"])
                )
                if start_key == "A" and end_key == "5":
                    print(
                        "BBB",
                        start_key,
                        end_key,
                        num_button_presses_for_start_and_end_keys[(start_key, end_key)],
                    )
# num_button_presses_for_start_and_end_keys
# %%
nrobots = 10
best_button_presses_for_start_and_end_num_keys = dict()
for button_pair, possible_paths in num_button_presses_for_start_and_end_keys.items():
    if len(possible_paths) == 1:
        best_path = list(list(possible_paths)[0])
    else:
        maxlength = 3424523524352343432432423
        for path in possible_paths:
            if button_pair == ("A", "5"):
                print(path)
            output_path_length = get_output_length_for_input_sequence(
                list(path), nrobots=10
            )
            if output_path_length < maxlength:
                maxlength = output_path_length
                best_path = list(path)
                if button_pair == ("A", "5"):
                    print("bbb", best_path)
    best_button_presses_for_start_and_end_num_keys[button_pair] = best_path

# %%
input_button_pairs_to_list_of_output_pairs = dict()
for (
    input_button_pair,
    output_sequence,
) in best_button_presses_for_start_and_end_keys.items():
    input_button_pairs_to_list_of_output_pairs[input_button_pair] = [
        (first, second)
        for (first, second) in zip(["A"] + output_sequence, output_sequence)
    ]
input_button_pairs_to_list_of_output_pairs
# %%
input_num_button_pairs_to_list_of_output_arrow_pairs = dict()
for (
    input_button_pair,
    output_sequence,
) in best_button_presses_for_start_and_end_num_keys.items():
    input_num_button_pairs_to_list_of_output_arrow_pairs[input_button_pair] = [
        (first, second)
        for (first, second) in zip(["A"] + output_sequence, output_sequence)
    ]
input_num_button_pairs_to_list_of_output_arrow_pairs


# %%
def get_first_sequence_pairs(keypad_input):
    first_full_sequence_pairs = []
    for first, second in zip(
        ["A"] + [x for x in keypad_input], [x for x in keypad_input]
    ):
        first_full_sequence_pairs += (
            input_num_button_pairs_to_list_of_output_arrow_pairs[(first, second)]
        )
    return first_full_sequence_pairs


def get_length_for_input(keypad_input, nrobots):
    first_full_sequence_pairs = get_first_sequence_pairs(keypad_input)
    return get_output_length_for_input_pairs(first_full_sequence_pairs, nrobots=nrobots)


def get_final_count(keypad_input, nrobots):
    return int(keypad_input.split("A")[0]) * get_length_for_input(
        keypad_input, nrobots=nrobots
    )


# %%

length_with_3_robots = partial(get_final_count, nrobots=2)
length_with_25_robots = partial(get_final_count, nrobots=25)
print(sum(map(length_with_3_robots, data)))
print(sum(map(length_with_25_robots, data)))

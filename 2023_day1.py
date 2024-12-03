# %%
from utils import load_advent_of_code

data = load_advent_of_code(20231)
# %%
import re

dd = ["".join(list(map(str, re.findall(r"\d+", line)))) for line in data]
ee = [int(line[0] + line[-1]) for line in dd]
sum(ee)

# sum([int("".join(list(map(str, re.findall(r"\d+", line))))) for line in data])


# %%
def find_number(line):
    subdict = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }
    for key in subdict:
        if line[0 : len(key)] == key:
            return subdict[key]
    return None


def subout(line):
    for line_iter in range(len(line)):
        first = find_number(line[line_iter:])
        if first:
            break
    for line_iter in range(1, len(line) + 1):
        last = find_number(line[-line_iter:])
        if last:
            break

    return int(first + last)


ee = [subout(line) for line in data]
sum(ee)

# %%

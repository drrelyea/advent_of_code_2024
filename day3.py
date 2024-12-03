# %%
from utils import load_advent_of_code

data = load_advent_of_code(20243)
# %%
import re


def find_valid_statements(line):
    valid = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", line)
    return valid


def find_valid_statements_and_positions(line):
    position_by_num = {}
    valid = re.finditer(r"mul\([0-9]{1,3},[0-9]{1,3}\)", line)
    for validmul in valid:
        position_by_num[validmul.start()] = {
            "value": validmul.group(),
        }
    return position_by_num


def find_do_statements_and_positions(line):
    start_positions = set()
    valid = re.finditer(r"do()", line)
    for validmul in valid:
        start_positions.add(validmul.start())
    return start_positions


def find_donot_statements_and_positions(line):
    start_positions = set()
    valid = re.finditer(r"don't()", line)
    for validmul in valid:
        start_positions.add(validmul.start())
    return start_positions


# %%
running_total = 0
alllines = "".join(data)
vsp = find_valid_statements_and_positions(alllines)
dosp = find_do_statements_and_positions(alllines)
donotsp = find_donot_statements_and_positions(alllines)
ignore = False
for ii in range(len(alllines)):
    if ii in donotsp:
        ignore = True
    elif ii in dosp:
        ignore = False
    elif ii in vsp and not ignore:
        ss = vsp[ii]["value"]
        running_total += int(ss.split("mul(")[1].split(",")[0]) * int(
            ss.split(",")[1].split(")")[0]
        )

print(running_total)
# %%

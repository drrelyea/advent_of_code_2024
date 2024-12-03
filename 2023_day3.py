# %%
from utils import load_advent_of_code

data = load_advent_of_code(20233)
# %%
import re


def find_number_and_its_position_in_line(line):
    position_by_num = {}
    allnums = re.finditer(r"\d+", line)
    for idd, dd in allnums:
        position_by_num[idd] = {
            "start": dd.start(),
            "end": dd.end(),
            "value": int(dd.group()),
        }
    return position_by_num


def find_symbol_and_its_position_in_line(line):
    position_by_num = {}
    allnums = re.finditer(r"\d+", line)
    for idd, dd in allnums:
        position_by_num[idd] = {
            "start": dd.start(),
            "end": dd.end(),
            "value": int(dd.group()),
        }
    return position_by_num


ss = 0
for line in data:
    aa = line.split(":")[1]
    if all([get_valid(subline) for subline in aa.split(";")]):
        ss += int(line.split("Game ")[1].split(":")[0])
print(ss)


# %%
def update_color_dict(colordict, line):
    for color in colordict:
        nn = get_number_for_color(line, color)
        if nn > colordict[color]:
            colordict[color] = nn
    return colordict


ss = 0
for line in data:
    colordict = {"red": 0, "green": 0, "blue": 0}
    for subline in line.split(":")[1].split(";"):
        colordict = update_color_dict(colordict, subline)
    ss += colordict["red"] * colordict["green"] * colordict["blue"]
print(ss)

# %%

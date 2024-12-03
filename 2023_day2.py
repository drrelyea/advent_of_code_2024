# %%
from utils import load_advent_of_code

data = load_advent_of_code(20232)
# %%


import re


def get_number_for_color(line, color):
    if color in line:
        if re.findall(r" \d+ " + color, line):
            nn = int(
                re.findall(r" \d+ " + color, line)[0].split(" " + color)[0].strip()
            )
            return nn
    return 0


def get_valid(line):
    colordict = {"blue": 14, "red": 12, "green": 13}

    for color in colordict:
        nn = get_number_for_color(line, color)
        if nn > colordict[color]:
            return False
    return True


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

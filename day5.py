# %%
import re

from utils import load_advent_of_code

data = load_advent_of_code(20245)
print(data)
# %%
rules = [line for line in data if "|" in line]
orders = list(line.split("|") for line in rules)
print(orders)
# %%
ss = 0
updates = [line for line in data if "," in line]
for line in updates:
    numbers = line.split(",")
    print(numbers)
    goodline = True
    for order in orders:
        first = order[0]
        second = order[1]
        if first in line and second in line:
            if line.index(first) > line.index(second):
                goodline = False
                break
    if goodline:
        ss += int(numbers[int((len(numbers) - 1) / 2)])

print(ss)
# %%
ss = 0
for line in updates:
    numbers = line.split(",")
    goodline = True
    for order in orders:
        first = order[0]
        second = order[1]
        if first in line and second in line:
            if line.index(first) > line.index(second):
                goodline = False
                break
    if not goodline:
        linecopy = line.split(",")
        newline = []
        while linecopy:
            linepoppy = linecopy.copy()
            for order in orders:
                if order[0] in linepoppy and order[1] in linepoppy:
                    linepoppy.remove(order[1])
            newline += linepoppy
            linecopy = [element for element in linecopy if element not in newline]
        ss += int(newline[int((len(newline) - 1) / 2)])
print(ss)
# %%

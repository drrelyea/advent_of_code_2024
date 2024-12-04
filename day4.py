# %%
from utils import load_advent_of_code

data = load_advent_of_code(20244)
print(data)
# %%
import re

xsum = 0
dd = list(zip(*data))
datatransposed = ["".join(ll) for ll in dd]

for line in data:
    xsum += len(re.findall("XMAS", line))
    xsum += len(re.findall("XMAS", line[::-1]))
for line in datatransposed:
    xsum += len(re.findall("XMAS", line))
    xsum += len(re.findall("XMAS", line[::-1]))

data_diag = []
for iline in range(2 * len(data)):
    new_array = []
    for jline in range(iline + 1):
        if jline < len(data) and iline - jline < len(data):
            new_array.append(data[jline][iline - jline])
    data_diag.append("".join(new_array))
for line in data_diag:
    xsum += len(re.findall("XMAS", line))
    xsum += len(re.findall("XMAS", line[::-1]))

data_diag = []
for iline in range(2 * len(data)):
    new_array = []
    for jline in range(iline + 1):
        if jline < len(data) and iline - jline < len(data):
            new_array.append(data[-1 - jline][iline - jline])
    data_diag.append("".join(new_array))
for line in data_diag:
    xsum += len(re.findall("XMAS", line))
    xsum += len(re.findall("XMAS", line[::-1]))

print(xsum)


# %%
def find_mas_in_3x3(data_block):
    return (
        data_block[0][0] == "M"
        and data_block[0][2] == "S"
        and data_block[1][1] == "A"
        and data_block[2][0] == "M"
        and data_block[2][2] == "S"
    )


def find_mas_in_3x3_permutations(data_block):
    qq = data_block.copy()
    dd = list(zip(*qq))
    datatransposed = ["".join(ll) for ll in dd]
    return (
        find_mas_in_3x3(data_block)
        or find_mas_in_3x3([line[::-1] for line in data_block])
        or find_mas_in_3x3(datatransposed)
        or find_mas_in_3x3([line[::-1] for line in datatransposed])
    )


xsum = 0
for ii in range(len(data) - 2):
    for jj in range(len(data) - 2):
        datablock = []
        datablock.append(data[ii][jj : jj + 3])
        datablock.append(data[ii + 1][jj : jj + 3])
        datablock.append(data[ii + 2][jj : jj + 3])
        if find_mas_in_3x3_permutations(datablock):
            xsum += 1
print(xsum)

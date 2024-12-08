# %%
import operator
from itertools import combinations

from utils import load_advent_of_code

data = load_advent_of_code(20247)
print(data)

# %%
letters = set("".join(data))
letters.remove(".")

# %%
subtract = lambda x, y: tuple(map(operator.sub, x, y))
add = lambda x, y: tuple(map(operator.add, x, y))
datasize = len(data)

partarange = [1]
partbrange = list(range(50))


def calculate_nnodes(therange):
    nodelist = set()
    for letter in letters:
        locationlist = []
        for iline, line in enumerate(data):
            for ill, lineletter in enumerate(line):
                if lineletter == letter:
                    locationlist.append((iline, ill))
        for pair in combinations(locationlist, 2):
            deltapos = subtract(pair[0], pair[1])
            for nodeiter in therange:
                newnode = subtract(pair[1], tuple([nodeiter * dd for dd in deltapos]))
                if 0 <= newnode[0] < datasize and 0 <= newnode[1] < datasize:
                    nodelist.add(newnode)
                else:
                    break
            for nodeiter in therange:
                newnode = add(pair[0], tuple([nodeiter * dd for dd in deltapos]))
                if 0 <= newnode[0] < datasize and 0 <= newnode[1] < datasize:
                    nodelist.add(newnode)
                else:
                    break
    print(len(nodelist))


calculate_nnodes(partarange)
calculate_nnodes(partbrange)

# %%

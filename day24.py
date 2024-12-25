# %%
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202424)
# data = [
#     "x00: 1",
#     "x01: 0",
#     "x02: 1",
#     "x03: 1",
#     "x04: 0",
#     "y00: 1",
#     "y01: 1",
#     "y02: 1",
#     "y03: 1",
#     "y04: 1",
#     "",
#     "ntg XOR fgs -> mjb",
#     "y02 OR x01 -> tnw",
#     "kwq OR kpj -> z05",
#     "x00 OR x03 -> fst",
#     "tgd XOR rvg -> z01",
#     "vdt OR tnw -> bfw",
#     "bfw AND frj -> z10",
#     "ffh OR nrd -> bqk",
#     "y00 AND y03 -> djm",
#     "y03 OR y00 -> psh",
#     "bqk OR frj -> z08",
#     "tnw OR fst -> frj",
#     "gnj AND tgd -> z11",
#     "bfw XOR mjb -> z00",
#     "x03 OR x00 -> vdt",
#     "gnj AND wpb -> z02",
#     "x04 AND y00 -> kjc",
#     "djm OR pbm -> qhw",
#     "nrd AND vdt -> hwm",
#     "kjc AND fst -> rvg",
#     "y04 OR y02 -> fgs",
#     "y01 AND x02 -> pbm",
#     "ntg OR kjc -> kwq",
#     "psh XOR fgs -> tgd",
#     "qhw XOR tgd -> z09",
#     "pbm OR djm -> kpj",
#     "x03 XOR y03 -> ffh",
#     "x00 XOR y04 -> ntg",
#     "bfw OR bqk -> z06",
#     "nrd XOR fgs -> wpb",
#     "frj XOR qhw -> z04",
#     "bqk OR frj -> z07",
#     "y03 OR x01 -> nrd",
#     "hwm AND bqk -> z03",
#     "tgd XOR rvg -> z12",
#     "tnw OR pbm -> gnj",
# ]
print(data)

nn = data_to_numpy(data)
# nn = nn.T

size = len(data)
# size = 71


# shapedict = dict()
# for ii in range(size):
#     for jj in range(size):
#         shapedict[(ii, jj)] = nn[(ii, jj)]


# %%
def myor(x, y):
    return x | y


def myand(x, y):
    return x & y


def myxor(x, y):
    return x ^ y


opmap = {"OR": myor, "XOR": myxor, "AND": myand}
initial_bits = defaultdict(int)
operations = list()
opdict = defaultdict(str)
for line in data:
    if ":" in line:
        initial_bits[line.split(":")[0]] = int(line.split(": ")[1])
    elif "->" in line:
        operations.append(
            (
                opmap[line.split(" ")[1]],
                line.split(" ")[0],
                line.split(" ")[2],
                line.split(" -> ")[1],
            )
        )
        opdict[(opmap[line.split(" ")[1]], line.split(" ")[0], line.split(" ")[2])] = (
            line.split(" -> ")[1]
        )
bits = initial_bits.copy()
# %%
ii = 0
sorted_ops = list()
oplen = len(operations)
while ii < oplen:
    for oo in operations:
        lastone = True
        for pp in operations:
            if oo[3] == pp[1] or oo[3] == pp[2]:
                lastone = False
                break
        if lastone:
            operations.remove(oo)
            sorted_ops.append(oo)
            ii += 1
            break
# %%
for op in sorted_ops[::-1]:
    bits[op[3]] = op[0](bits[op[1]], bits[op[2]])
num = 0
for bit, value in bits.items():
    if bit.startswith("z"):
        print(bit, value)
        num += (2 ** int(bit[1:])) * value
print(num)
# %%

# ok game plan
# we iterate upwards
# addition is 00 0 01 1 10 1 11 0 so it is XOR and then carry up AND
# for each, we figure out what led to it
# and if something led to it, awesome
for ii in range(45):
    possiblex = [0, 1]
    possibley = [0, 1]
    possibler = [0, 1]
    bits = initial_bits.copy()
    for qq in range(45):
        bits["x" + f"{qq:02}"] = 0
        bits["y" + f"{qq:02}"] = 0
    for xx in [0, 1]:
        for yy in [0, 1]:
            for rr in [0, 1]:
                bits["x" + f"{ii:02}"] = xx
                bits["y" + f"{ii:02}"] = yy
                if ii != 0 and rr == 0:
                    bits["x" + f"{(ii-1):02}"] = 0
                    bits["y" + f"{(ii-1):02}"] = 0
                if ii != 0 and rr == 1:
                    bits["x" + f"{(ii-1):02}"] = 1
                    bits["y" + f"{(ii-1):02}"] = 1
                for op in sorted_ops[::-1]:
                    bits[op[3]] = op[0](bits[op[1]], bits[op[2]])
                if ii == 0:
                    if bits["z" + f"{ii:02}"] != (xx ^ yy):
                        print("bad for ", ii, xx, yy, rr)
                else:
                    if bits["z" + f"{ii:02}"] != (xx ^ yy) ^ rr:
                        print("bad for ", ii, xx, yy, rr)


# 7 8 13 14 24 25 31
# %%
# LOL MANUAL

bgs,pqc,rjm,swt,wsv,z07,z13,z31

]
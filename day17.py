# %%
import re
from dataclasses import dataclass
from functools import cache

import numpy as np

from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202416)

print(data)

nn = data_to_numpy(data)
# nn = nn.T

size = len(data)


# shapedict = dict()
# for ii in range(size):
#     for jj in range(size):
#         shapedict[(ii, jj)] = nn[(ii, jj)]


# %%
def combo(opcode, memory):
    if opcode < 4:
        return opcode
    if 4 <= opcode <= 6:
        return memory[opcode - 4]

# 0
def adv(operand, memory, instruction_pointer):
    memory[0] = memory[0] // 2 ** combo(operand, memory)
    instruction_pointer += 2
    return memory, instruction_pointer

# 1
def bxl(operand, memory, instruction_pointer):
    memory[1] = memory[1] ^ operand
    instruction_pointer += 2
    return memory, instruction_pointer

# 2
def bst(operand, memory, instruction_pointer):
    memory[1] = combo(operand, memory) % 8
    instruction_pointer += 2
    return memory, instruction_pointer

# 3
def jnz(operand, memory, instruction_pointer):
    if memory[0] != 0:
        instruction_pointer = operand
    else:
        instruction_pointer += 2
    return memory, instruction_pointer

# 4
def bxc(operand, memory, instruction_pointer):
    memory[1] = memory[1] ^ memory[2]
    instruction_pointer += 2
    return memory, instruction_pointer

# 5
def oot(operand, memory, instruction_pointer):
    memory[3].append(combo(operand, memory) % 8)
    instruction_pointer += 2
    return memory, instruction_pointer

# 6
def bdv(operand, memory, instruction_pointer):
    memory[1] = memory[0] // 2 ** combo(operand, memory)
    instruction_pointer += 2
    return memory, instruction_pointer

# 7
def cdv(operand, memory, instruction_pointer):
    memory[2] = memory[0] // 2 ** combo(operand, memory)
    instruction_pointer += 2
    return memory, instruction_pointer


opcode_to_fxn = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: oot,
    6: bdv,
    7: cdv,
}


def run_code(opcode, operand, memory, instruction_pointer):
    return opcode_to_fxn[opcode](operand, memory, instruction_pointer)


def execute_program(input_sequence, memory, debug=False):
    program = [int(x) for x in input_sequence.split(",")]
    instruction_pointer = 0
    while instruction_pointer >= 0 and instruction_pointer < len(program):
        memory, instruction_pointer = run_code(
            program[instruction_pointer],
            program[instruction_pointer + 1],
            memory,
            instruction_pointer,
        )
        if(debug):
            print(memory)


# %%
fake_memory = [None] * 4
fake_memory[3] = []

fake_memory[0] = 117440
fake_memory[1] = 0
fake_memory[2] = 0
input_string = "0,3,5,4,3,0"
execute_program(input_string, fake_memory)
output_string = ",".join([str(x) for x in fake_memory[3]])
output_string == input_string

# %%
real_memory = [None] * 4
real_memory[3] = []

real_memory[0] = int(data[0].split(": ")[1])
real_memory[1] = 0
real_memory[2] = 0
input_string = data[4].split(": ")[1]
print(real_memory, input_string)
execute_program(input_string, real_memory)
print(real_memory)
print(",".join([str(x) for x in real_memory[3]]))


# %%
input_string = data[4].split(": ")[1]
outputs_per_input = dict()
for ii in range(4096):
    real_memory = [ii, 0, 0, []]
    execute_program(input_string, real_memory)
    output_string = ",".join([str(x) for x in real_memory[3]])
    outputs_per_input[((ii // 512) % 8, (ii // 64) % 8, (ii // 8) % 8, ii % 8)] = output_string

# %%
input_characters = input_string.split(",")
ind = 0

# for each character, you have the sequences that could have put out the prior character
# for all of those shifted by 8, you figure out the ones that could have put out the next

# %%
first_character = input_characters[0]
possible_input_sequences = [
    input_sequence for input_sequence, output_sequence in outputs_per_input.items() if output_sequence[0] == first_character
]
for icharacter, character in enumerate(input_characters):
    if icharacter == 0:
        possible_input_sequences = [
            input_sequence for input_sequence, output_sequence in outputs_per_input.items() if output_sequence[0] == character
        ]
    else:
        new_possible_input_sequences = list()
        for possible_sequence in possible_input_sequences:
            if icharacter >= len(input_characters) - 3:
                rangelen = 1
            else:
                rangelen = 8
            for ii in range(rangelen):
                new_input_sequence = (ii, ) + possible_sequence[0:3]
                if outputs_per_input[new_input_sequence][0] == character:
                    new_possible_input_sequences.append((ii,) + possible_sequence)
        possible_input_sequences = new_possible_input_sequences
    print(icharacter, len(possible_input_sequences))

# %%           

maxnum = 5478357843857439593
for line in possible_input_sequences:
    number = sum([line[-ii-1]*(8**ii) for ii in range(len(line))])
    if number < maxnum:
        maxnum = number
print(maxnum)

# %%
for ii in range(8):
    for jj in range(8):
        for kk in range(8):
            for ll in range(8):
                for possible_sequence in possible_input_sequences:
                    number = sum([line[-ii-1]*(8**ii) for ii in range(len(possible_sequence)-7)])
                    newnumber = ll*8**12 + kk*8**13 + jj*8**14 + ii*8**15 + number
                    real_memory = [None] * 4
                    real_memory = [newnumber,0,0,[]]
                    execute_program(input_string, real_memory)
                    output_string = ",".join([str(x) for x in real_memory[3]])
                    # print(len(output_string), len(input_string))
                    if output_string == input_string:
                        print(newnumber)

# %%
for possible_sequence in possible_input_sequences:
    number = sum([possible_sequence[-ii-1]*(8**ii) for ii in range(len(possible_sequence))])
    print(number)
    newnumber = number
    real_memory = [None] * 4
    real_memory = [newnumber,0,0,[]]
    execute_program(input_string, real_memory)
    output_string = ",".join([str(x) for x in real_memory[3]])
    # print(len(output_string), len(input_string))
    print(possible_sequence, output_string, number)
    # if output_string == input_string:
    #     print(newnumber)

# %%
qq = possible_input_sequences[0]
number = sum([qq[-ii-1]*(8**ii) for ii in range(len(qq))])



# %%
for ichar, input_character in enumerate(input_characters):
    possible_sequences = dict()
    for input_sequence, output_sequence in outputs_per_input.items():
        if ichar == 0:
            if output_sequence[0] == input_character:
                possible_sequences[input_sequence] = output_sequence
        else:
            if output_sequence[0] == input_character and output_sequence
        if outputs_per_input[0] == input_character and SOMETHING:
            possible_sequences[]

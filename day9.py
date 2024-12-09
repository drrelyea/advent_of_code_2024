# %%
import numpy as np
from utils import data_to_numpy, load_advent_of_code

data = load_advent_of_code(20249)
print(data)

# %%
nn = data_to_numpy(data)

# %%
fileID = 0
index = 0
isfile = True
totallength = sum([int(xx) for xx in data[0]])
register = np.zeros(totallength) - 1
total_nonzero = 0
for nn in data[0]:
    nnn = int(nn)
    if isfile:
        register[index : index + nnn] = fileID
        index += nnn
        total_nonzero += nnn
        fileID += 1
        isfile = False
    else:
        index += nnn
        isfile = True
# %%
endindex = -1
for qq in range(totallength):
    if register[qq] != -1:
        continue
    else:
        if total_nonzero - endindex == totallength + 1:
            break
        while register[endindex] == -1:
            endindex -= 1
        register[qq] = register[endindex]
        register[endindex] = -1
        endindex -= 1
checksum = 0
for qq in range(totallength):
    if register[qq] != -1:
        checksum += register[qq] * qq
print(checksum)

# %%
all_files = dict()
all_gaps = dict()
gap_lengths = dict()
fileID = 0
index = 0
isfile = True
totallength = sum([int(xx) for xx in data[0]])
total_nonzero = 0
gapID = 0
for nn in data[0]:
    blocklength = int(nn)
    if isfile:
        all_files[fileID] = (index, blocklength)
        index += blocklength
        total_nonzero += blocklength
        fileID += 1
        isfile = False
    else:
        all_gaps[gapID] = (index, blocklength)
        if blocklength in gap_lengths:
            gap_lengths[blocklength].append(index)
        else:
            gap_lengths[blocklength] = [index]
        index += blocklength
        gapID += 1
        isfile = True
maxfileID = fileID - 1

endindex = -1
fileID = maxfileID
while fileID > 0:
    for gap in all_gaps:
        if all_gaps[gap][0] > all_files[fileID][0]:
            break
        if all_gaps[gap][1] >= all_files[fileID][1]:
            all_files[fileID] = (all_gaps[gap][0], all_files[fileID][1])
            if all_gaps[gap][1] == all_files[fileID][1]:
                del all_gaps[gap]
            else:
                all_gaps[gap] = (
                    all_gaps[gap][0] + all_files[fileID][1],
                    all_gaps[gap][1] - all_files[fileID][1],
                )
            break
    fileID -= 1

checksum = 0
for fileID in all_files:
    for index in range(all_files[fileID][1]):
        checksum += fileID * (all_files[fileID][0] + index)
print(checksum)

# %%

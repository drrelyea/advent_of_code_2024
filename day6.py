# %%
import re

from utils import load_advent_of_code

data = load_advent_of_code(20245)
print(data)
for iline, line in enumerate(data):
    if "^" in line:
        starty = iline
        startx = line.index("^")
        break


# %%
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
mapsize = len(data)


def go_through_maze(data):
    loop = False
    currx = startx
    curry = starty
    positions = dict()
    dirpointer = 0
    while 0 <= currx < mapsize and 0 <= curry < mapsize:
        currv = directions[dirpointer]
        # print(positions)
        if (currx, curry) in positions:
            if currv in positions[(currx, curry)]:
                loop = True
                break
            else:
                positions[(currx, curry)].append(currv)
        else:
            positions[(currx, curry)] = [currv]

        newy = curry + currv[0]
        newx = currx + currv[1]
        if 0 <= newy < mapsize and 0 <= newx < mapsize and datacopy[newy][newx] == "#":
            dirpointer = (dirpointer + 1) % 4
        else:
            curry = newy
            currx = newx
    return positions, loop


positions, loop = go_through_maze(data)

print(len(positions))
# %%
loopsum = 0
mapsize = len(data)
oldtrack = positions
del oldtrack[(startx, starty)]
for jj, ii in oldtrack:
    if data[ii][jj] != "#":
        datacopy = data.copy()
        datacopy[ii] = datacopy[ii][0:jj] + "#" + datacopy[ii][jj + 1 :]
        positions, loop = go_through_maze(datacopy)

        if loop:
            loopsum += 1

print(loopsum)
# %%

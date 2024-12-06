# %%
import re

from utils import load_advent_of_code

data = load_advent_of_code(20245)
print(data)
# %%
# data = [
#     "....#.....",
#     ".........#",
#     "..........",
#     "..#.......",
#     ".......#..",
#     "..........",
#     ".#..^.....",
#     "........#.",
#     "#.........",
#     "......#...",
# ]
for iline, line in enumerate(data):
    if "^" in line:
        starty = iline
        startx = line.index("^")
        break


# %%
currx = startx
curry = starty
currv = "up"
positions = dict()
mapsize = len(data)
while 0 <= currx < mapsize and 0 <= curry < mapsize:
    # print(positions)
    if (currx, curry) in positions:
        if currv in positions[(currx, curry)]:
            break
        else:
            positions[(currx, curry)].append(currv)
    else:
        positions[(currx, curry)] = [currv]

    if currv == "up":
        if curry == 0:
            break
        if data[curry - 1][currx] == "#":
            currv = "right"
        else:
            curry -= 1
    elif currv == "down":
        if curry == mapsize - 1:
            break
        if data[curry + 1][currx] == "#":
            currv = "left"
        else:
            curry += 1
    elif currv == "right":
        if currx == mapsize - 1:
            break
        if data[curry][currx + 1] == "#":
            currv = "down"
        else:
            currx += 1
    elif currv == "left":
        if currx == 0:
            break
        if data[curry][currx - 1] == "#":
            currv = "up"
        else:
            currx -= 1

print(len(positions))
# %%
loopsum = 0
mapsize = len(data)
for ii in range(mapsize):
    for jj in range(mapsize):
        if data[ii][jj] != "#":
            currx = startx
            curry = starty
            currv = "up"
            positions = dict()
            datacopy = data.copy()
            datacopy[ii] = datacopy[ii][0:jj] + "#" + datacopy[ii][jj + 1 :]
            loop = False
            while 0 <= currx < mapsize and 0 <= curry < mapsize:
                # print(positions)
                if (currx, curry) in positions:
                    if currv in positions[(currx, curry)]:
                        loop = True
                        break
                    else:
                        positions[(currx, curry)].append(currv)
                else:
                    positions[(currx, curry)] = [currv]

                if currv == "up":
                    if curry == 0:
                        break
                    if datacopy[curry - 1][currx] == "#":
                        currv = "right"
                    else:
                        curry -= 1
                elif currv == "down":
                    if curry == mapsize - 1:
                        break
                    if datacopy[curry + 1][currx] == "#":
                        currv = "left"
                    else:
                        curry += 1
                elif currv == "right":
                    if currx == mapsize - 1:
                        break
                    if datacopy[curry][currx + 1] == "#":
                        currv = "down"
                    else:
                        currx += 1
                elif currv == "left":
                    if currx == 0:
                        break
                    if datacopy[curry][currx - 1] == "#":
                        currv = "up"
                    else:
                        currx -= 1
            if loop:
                loopsum += 1

# %%

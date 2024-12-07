# %%
from utils import load_advent_of_code

data = load_advent_of_code(20247)
print(data)

# %%
ops = ("+", "*")
validsum = 0
for line in data:
    thesum = int(line.split(":")[0])
    numbers = [int(x) for x in line.split(" ")[1:]]
    for i in range(2 ** (len(numbers) - 1)):
        thepartialsequence = [int(x) for x in bin(i).split("b")[1]]
        extralength = len(numbers) - 1 - len(thepartialsequence)
        thesequence = [0] * extralength + thepartialsequence
        total = 0
        for inum, num in enumerate(numbers):
            if inum == 0:
                total = num
            else:
                if thesequence[inum - 1] == 0:
                    total += num
                else:
                    total *= num
        if total == thesum:
            validsum += thesum
            break


# %%
def ternary(n):
    if n == 0:
        return "0"
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return "".join(reversed(nums))


ops = ("+", "*")
validsum = 0
for line in data:
    thesum = int(line.split(":")[0])
    numbers = [int(x) for x in line.split(" ")[1:]]
    for i in range(3 ** (len(numbers) - 1)):
        thepartialsequence = [int(x) for x in ternary(i)]
        extralength = len(numbers) - 1 - len(thepartialsequence)
        thesequence = [0] * extralength + thepartialsequence
        total = 0
        for inum, num in enumerate(numbers):
            if inum == 0:
                total = num
            else:
                if thesequence[inum - 1] == 0:
                    total += num
                elif thesequence[inum - 1] == 1:
                    total *= num
                else:
                    total = int(str(total) + str(num))
            if total > thesum:
                break
        if total == thesum:
            validsum += thesum
            break
print(validsum)

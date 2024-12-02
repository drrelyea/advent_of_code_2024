# %%
from utils import load_advent_of_code

data = load_advent_of_code(2)
# %%
dd = [list(map(int, line.split())) for line in data]


# %%
def is_line_safe(line):
    safeint = 1
    direction = 0
    if len(line) > 1:
        if line[1] > line[0]:
            direction = 1
        elif line[1] < line[0]:
            direction = -1
    for ii, iin in zip(line[:-1], line[1:]):
        if direction == 1 and not (1 <= iin - ii <= 3):
            safeint = 0
        elif direction == -1 and not (1 <= ii - iin <= 3):
            safeint = 0
        elif direction == 0:
            safeint = 0
    return safeint


def is_line_safe2(line):
    if line != sorted(line) and line != sorted(line)[::-1]:
        return 0
    if any(
        [not (1 <= abs(ii - iinext) <= 3) for ii, iinext in zip(line[:-1], line[1:])]
    ):
        return 0
    return 1


safe = sum(map(is_line_safe2, dd))
print(safe)
# %%


def is_line_almost_safe(line):
    return any(
        is_line_safe(line[0:removed_element] + line[removed_element + 1 :])
        for removed_element in range(len(line))
    )


safe = sum(map(is_line_almost_safe, dd))
print(safe)
# %%

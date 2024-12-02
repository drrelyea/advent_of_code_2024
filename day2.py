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


safe = 0
for line in dd:
    safe += is_line_safe(line)
print(safe)
# %%

safe = 0
for line in dd:
    for removed_element in range(len(line)):
        newline = line[0:removed_element] + line[removed_element + 1 :]
        if is_line_safe(newline):
            safe += 1
            break
print(safe)
# %%

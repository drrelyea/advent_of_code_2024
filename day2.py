# %%
from utils import load_advent_of_code

data = load_advent_of_code(2)
# %%
data = [line.split() for line in data]
dd = []
for line in data:
    dd.append([int(aa) for aa in line])
# %%
safe = 0
for line in dd:
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
    print(line, safeint)
    safe += safeint
# %%

qq = 0
for fff, sss in zip(ff, ss):
    print(fff, sss, abs(fff - sss))
    qq += abs(fff - sss)
print(qq)
# current_sum = 0
# max_sum = 0
# for line in data:
#     if line:
#         current_sum += int(line)
#     else:
#         max_sum = max(max_sum, current_sum)
#         current_sum = 0

# %%
qq = 0
for fff in ff:
    qq += fff * ss.count(fff)
print(qq)
# %%

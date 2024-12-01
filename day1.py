# %%
from utils import load_advent_of_code

data = load_advent_of_code(1)
# %%
firstcol = [int(line.split("   ")[0]) for line in data]
secondcol = [int(line.split("   ")[1]) for line in data]

ff = sorted(firstcol)
ss = sorted(secondcol)

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

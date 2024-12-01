# %%
import torch
from utils import load_advent_of_code

data = load_advent_of_code(1)

# %%
device = torch.device("mps")
tt = torch.tensor(
    [[int(element) for element in line.split()] for line in data], device=device
)

# %%
tt0 = tt[:, 0].sort()[0]
tt1 = tt[:, 1].sort()[0]
print(torch.sum(torch.abs(tt0 - tt1)))
# %%
unique_values, counts = torch.unique(tt1, return_counts=True)

qq = 0
for uu, cc in zip(unique_values, counts):
    if uu in tt0:
        qq += uu * cc

# %%

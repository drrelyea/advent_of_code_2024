# %%
from collections import defaultdict
from heapq import heappop, heappush

from utils import load_advent_of_code

data = load_advent_of_code(202420)

grid = {i + j * 1j: c for i, r in enumerate(data) for j, c in enumerate(r) if c != "#"}

(start_pos,) = (p for p in grid if grid[p] in "S")
(end_pos,) = (p for p in grid if grid[p] in "E")

front_flood_scores = defaultdict(lambda: 1e9)
end_flood_scores = defaultdict(lambda: 1e9)


def solve_maze(start, end, flood_scores):
    shortest_path = 1e9
    unexplored_points = [(0, t := 0, start, [start])]
    while unexplored_points:
        score, _, pos, path = heappop(unexplored_points)

        if score > flood_scores[pos]:
            continue
        flood_scores[pos] = score

        if pos == end and score <= shortest_path:
            shortest_path = score

        for dpos in [1, -1, 1j, -1j]:
            new = pos + dpos
            if new in grid and new not in path:
                heappush(unexplored_points, (score + 1, t := t + 1, new, path + [new]))
    return shortest_path, flood_scores


shortest_path_front, front_flood_scores = solve_maze(
    start_pos, end_pos, front_flood_scores
)
shortest_path_end, end_flood_scores = solve_maze(end_pos, start_pos, end_flood_scores)


def count_cheats(distance):
    cheatcounter = 0
    for front_pos, front_score in front_flood_scores.items():
        for end_pos, end_score in end_flood_scores.items():
            diff = front_pos - end_pos
            if abs(diff.real) + abs(diff.imag) <= distance:
                if (
                    front_score + end_score + abs(diff.real) + abs(diff.imag) - 1
                    <= shortest_path_front - 100
                ):
                    cheatcounter += 1
    print(cheatcounter)


count_cheats(2)
count_cheats(20)

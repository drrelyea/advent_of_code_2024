# %%
from dataclasses import dataclass

import numpy as np
from utils import data_to_numpy, get_indices_from_numpy, load_advent_of_code

data = load_advent_of_code(202410)
print(data)


nn = data_to_numpy(data, output_type=int)

zero_indices = get_indices_from_numpy(nn, 0)

surrounding_coordinates = ((0, 1), (0, -1), (1, 0), (-1, 0))
# %%


def find_next_number_in_path(data, xx, yy, number):
    all_endings = list()
    for coordinate in surrounding_coordinates:
        newxx = xx + coordinate[0]
        newyy = yy + coordinate[1]
        if 0 <= newxx < data.shape[0] and 0 <= newyy < data.shape[1]:
            # print(xx, yy, newxx, newyy, data[newxx, newyy])
            if data[newxx, newyy] == number:
                if number == 9:
                    the_tuple = (newxx, newyy)
                    yield [the_tuple]
                else:
                    for valid_ending in find_next_number_in_path(
                        data, newxx, newyy, number + 1
                    ):
                        if valid_ending:
                            for element in valid_ending:
                                all_endings.append(element)
    yield all_endings


# %%
totallist = dict()
for index in zero_indices:
    # if (
    #     index[0] == 0
    #     or index[1] == 0
    #     or index[0] == nn.shape[0] - 1
    #     or index[0] == nn.shape[1] - 1
    # ):
    if True:
        totallist[tuple(index)] = list(
            find_next_number_in_path(nn, index[0], index[1], 1)
        )

list_no_dupes = dict()
total_number = 0
for start, end in totallist.items():
    print(start)
    print(end)
    list_no_dupes[start] = set(end[0])
    total_number += len(list_no_dupes[start])
print(list_no_dupes)
print(total_number)


# %%
@dataclass(frozen=True)
class Point:
    x: int
    y: int


THIS CODE WORKED AND IS NOT CURRENTLY FUNCTIONAL BECAUSE I WAS REFACTORING

zero_index_points = [Point(x, y) for x, y in zero_indices.tolist()]


def add_points(p1: Point, p2: Point) -> Point:
    return Point(p1.x + p2.x, p1.y + p2.y)


def is_valid_point(p: Point, the_shape):
    return 0 <= p.x < the_shape[0] and 0 <= p.y < the_shape[1]


surrounding_coordinates = (Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0))


def find_next_number_in_full_path(
    data, point, number, all_paths_to_here: tuple[tuple[Point]]
):
    for coordinate in surrounding_coordinates:
        new_point = add_points(point, coordinate)
        if is_valid_point(new_point, data.shape):
            if data[new_point.x, new_point.y] == number:
                the_new_point = (new_point,)
                if number == 9:
                    all_final_paths = tuple()
                    for path in all_paths_to_here:
                        new_path = ((path + the_new_point),)
                        all_final_paths += new_path
                    yield all_final_paths
                else:
                    new_all_paths = tuple()
                    for path in all_paths_to_here:
                        new_all_paths += ((path + the_new_point),)
                    for allpaths in find_next_number_in_full_path(
                        data, new_point, number + 1, new_all_paths
                    ):
                        yield allpaths


# %%
starting_point = Point(0, 0)
all_starting_paths = ((starting_point,),)
for iqq, qq in enumerate(
    find_next_number_in_full_path(
        nn, starting_point.x, starting_point.y, 1, all_starting_paths
    )
):
    print(qq)
print(iqq)

# %%
totallist = dict()
for starting_point in zero_index_points:
    all_starting_paths = ((starting_point,),)
    totallist[tuple(index)] = list(
        find_next_number_in_full_path(nn, starting_point, 1, all_starting_paths)
    )

# %%
n_trailheads = 0
for key in totallist:
    n_trailheads += len(totallist[key])
    print(key, len(totallist[key]))
print(n_trailheads)

# %%

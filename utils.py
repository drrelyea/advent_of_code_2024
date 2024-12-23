from pathlib import Path
from typing import Optional

import numpy as np


def load_advent_of_code(the_day: int) -> list[str]:
    download_data_path = Path("/Users/relyea/Downloads/input.txt")
    other_download_data_path = Path("/Users/relyea/Downloads/input")
    local_data_path = (
        "/Users/relyea/code/advent_of_code_2024/input" + str(the_day) + ".txt"
    )
    if download_data_path.exists():
        download_data_path.rename(local_data_path)
    elif other_download_data_path.exists():
        other_download_data_path.rename(local_data_path)
    with open(local_data_path) as input_file:
        inpstring = input_file.readlines()

    data = [line.strip() for line in inpstring]
    return data


def data_to_numpy(
    thedata: list[str],
    output_type: type = str,
    delimiter: Optional[str] = None,
    pad_lines: bool = True,
):
    if not thedata:
        raise ValueError("data is null")
    if delimiter:
        xlen = 0
        for line in thedata:
            linelen = len(line.split(delimiter))
            if linelen > xlen:
                xlen = linelen
    else:
        xlen = len(thedata[0])
        for line in thedata:
            if len(line) != xlen and not pad_lines:
                raise ValueError("NOT ALL LINES THE SAME LENGTH!")
            if len(line) > xlen:
                xlen = len(line)
    padded_data = []
    for line in thedata:
        if delimiter:
            newline = line.split(delimiter)
        else:
            newline = [x for x in line]
        newline = [output_type(x) for x in newline]
        if pad_lines:
            if output_type is str:
                for _ in range(xlen - len(newline)):
                    newline.append("\x01")
            else:
                for _ in range(xlen - len(newline)):
                    newline.append(-99999)
        padded_data.append(newline)

    newdata = np.array(padded_data, dtype=output_type)
    return newdata


def get_indices_from_numpy(data, query):
    two_arrays = np.where(data == query)
    zipped_arrays = [(x, y) for (x, y) in zip(two_arrays[0], two_arrays[1])]
    return np.array(zipped_arrays, dtype=int)

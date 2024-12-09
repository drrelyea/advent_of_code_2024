import numpy as np
import pytest
from utils import data_to_numpy, get_indices_from_numpy


@pytest.fixture
def normal_data_rectangular():
    return [
        "f3q.qf4.fwgreg.qg",
        "fg.hh/4qgggegearv",
        "jh75ehEHG43wg//..",
        "FRWFAVrag...,rgae",
    ]


@pytest.fixture
def normal_data_varied_length():
    return [
        "f3q.qf4.feg.qg",
        "fg.hh/4qggegearv",
        "jh75ehEHG43wg//..",
        "FRWg...,rgae",
    ]


@pytest.fixture
def normal_data_square():
    return [
        "f3q.",
        "fg.h",
        "jh75",
        "FRWF",
    ]


@pytest.fixture
def numerical_data():
    return ["54365632", "65326435", "76547645", "22415213", "76574566"]


@pytest.fixture
def delimited_data(normal_data_varied_length):
    return [",".join(line) for line in normal_data_varied_length]


@pytest.fixture
def delimited_numerical_data():
    return [
        "431,4435,4353,321,3211,432432",
        "4634531,4435254235,43543553,323421,32154351,423432432",
        "4543531,44454335,46743353,354321,3654211,432765432"
        "435471,76544435,4765353,376521,32765411,47452432",
        "476575731,4745435,43765453,327651,327567411,432465732",
    ]


def test_square_data_to_numpy(normal_data_square):
    output_type = str
    delimiter = None
    line_padding = True
    qq = data_to_numpy(
        thedata=normal_data_square,
        output_type=output_type,
        delimiter=delimiter,
        pad_lines=line_padding,
    )
    assert type(qq) is np.ndarray
    assert qq.shape[0] == qq.shape[1]
    assert qq.dtype == "<U1"


def test_rectangular_data_to_numpy(normal_data_rectangular):
    output_type = str
    delimiter = None
    line_padding = True
    qq = data_to_numpy(
        thedata=normal_data_rectangular,
        output_type=output_type,
        delimiter=delimiter,
        pad_lines=line_padding,
    )
    assert type(qq) is np.ndarray
    assert qq.shape[0] != qq.shape[1]
    assert qq.dtype == "<U1"


def test_varied_data_to_numpy(normal_data_varied_length):
    output_type = str
    delimiter = None
    line_padding = True
    qq = data_to_numpy(
        thedata=normal_data_varied_length,
        output_type=output_type,
        delimiter=delimiter,
        pad_lines=line_padding,
    )
    assert type(qq) is np.ndarray
    assert qq.shape[0] != qq.shape[1]
    assert qq.dtype == "<U1"

    line_padding = False
    with pytest.raises(ValueError):
        qq = data_to_numpy(
            thedata=normal_data_varied_length,
            output_type=output_type,
            delimiter=delimiter,
            pad_lines=line_padding,
        )


def test_numerical_data_to_numpy(numerical_data):
    output_type = int
    delimiter = None
    line_padding = True
    qq = data_to_numpy(
        thedata=numerical_data,
        output_type=output_type,
        delimiter=delimiter,
        pad_lines=line_padding,
    )
    assert type(qq) is np.ndarray
    assert qq.shape[0] != qq.shape[1]
    assert qq.dtype == "int"


def test_delimited_data_to_numpy(delimited_data):
    output_type = str
    delimiter = ","
    line_padding = True
    qq = data_to_numpy(
        thedata=delimited_data,
        output_type=output_type,
        delimiter=delimiter,
        pad_lines=line_padding,
    )
    assert type(qq) is np.ndarray
    assert qq.shape[0] != qq.shape[1]
    assert qq.dtype == "<U1"

    line_padding = False
    with pytest.raises(ValueError):
        qq = data_to_numpy(
            thedata=delimited_data,
            output_type=output_type,
            delimiter=delimiter,
            pad_lines=line_padding,
        )


def test_delimited_numerical_data_to_numpy(delimited_numerical_data):
    output_type = int
    delimiter = ","
    line_padding = True
    qq = data_to_numpy(
        thedata=delimited_numerical_data,
        output_type=output_type,
        delimiter=delimiter,
        pad_lines=line_padding,
    )
    assert type(qq) is np.ndarray
    assert qq.shape[0] != qq.shape[1]
    assert qq.dtype == "int"

    line_padding = False
    with pytest.raises(ValueError):
        qq = data_to_numpy(
            thedata=delimited_numerical_data,
            output_type=output_type,
            delimiter=delimiter,
            pad_lines=line_padding,
        )


def test_get_indices_from_numpy(numerical_data):
    numpy_data = data_to_numpy(numerical_data, output_type=int)
    indices = get_indices_from_numpy(numpy_data, 7)
    print(indices)
    assert np.all(indices == np.array([[2, 0], [2, 4], [4, 0], [4, 3]]))

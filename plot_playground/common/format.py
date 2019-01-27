"""
A module that handles formats such as numbers.
"""

import enum

import numpy as np


class FORMAT(enum.IntEnum):
    """
    An enum class that handles numeric formats.

    Attribute
    ---------
    INT : int
        Integer format. e.g. 10
    FLOAT_1 : int
        Numbers up to the first decimal place. e.g. 10.5
    FLOAT_2 : int
        Numbers up to the second decimal place. e.g. 10.05
    FLOAT_3 : int
        Numbers up to the third decimal place. e.g. 10.005
    """
    INT = 1
    FLOAT_1 = 2
    FLOAT_2 = 3
    FLOAT_3 = 4


def convert_list_value_by_format(data_list, format):
    """
    Convert the number in the list to a value according to the
    specified format.

    Parameters
    ----------
    data_list : list
        A one-dimensional list containing numbers.
    format : int
        Number format. Specify the value of enum of FORMAT.

    Returns
    -------
    data_list : list
        A list containing the converted values.

    Raises
    ------
    ValueError
        If an incompatible format is specified.
    """
    if format == FORMAT.INT:
        data_arr = np.array(data_list)
        data_arr = data_arr.astype(np.int, copy=False)
        return data_arr.tolist()
    if format == FORMAT.FLOAT_1:
        data_list = [float('%.1f' % x) for x in data_list]
        return data_list
    if format == FORMAT.FLOAT_2:
        data_list = [float('%.2f' % x) for x in data_list]
        return data_list
    if format == FORMAT.FLOAT_3:
        data_list = [float('%.3f' % x) for x in data_list]
        return data_list
    err_msg = 'A value in an unsupported format is specified %s' % format
    raise ValueError(err_msg)

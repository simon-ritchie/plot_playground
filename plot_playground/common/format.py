"""
A module that handles formats such as numbers.
"""

import enum


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

"""
A module that handles the vertical axis elements of D3.js.
"""

import numpy as np

from plot_playground.common.format import FORMAT, convert_list_value_by_format
from plot_playground.common import d3_helper


def get_vaxis_script_str(
        svg_id, data_list, ticks=None, format=None, prefix_str=None,
        suffix_str=None):
    """
    Get the character string of the script for setting the vertical axis.

    Parameters
    ----------
    svg_id : str
        ID of the SVG to which the axis is added.
    data_list : list
        A one-dimensional list containing numbers.
    ticks : int or None, default None
        Number of axis ticks. When specifying, it is not necessarily the
        same number. It is set with easy-to-see numbers.
    format : int or None
        Number format. To make it easy to see, set a suitable value according
        6to dataset. The following types are allowed.
        - FORMAT.INT -> e.g. 10
        - FORMAT.FLOAT_1 -> e.g. 10.5
        - FORMAT.FLOAT_2 -> e.g. 10.55
        - FORMAT.FLOAT_3 -> e.g. 10.555
    prefix_str : str or None
        A character string given to the beginning of the axis. For example,
        if you set the '$' symbol, the axis labels are displayed like $ 100.
    suffix_str : str or None
        A character string appended to the end of the axis label. For example,
        if the '%' symbol is set, the axis label is displayed as 50%, and so on.

    Returns
    -------
    script_str : str
        A character string of the script for D3.js generated according
        to the setting.
    """
    format = FORMAT(format)
    data_list = convert_list_value_by_format(data_list=data_list, format=format)
    y_baseline = _get_y_baseline(data_list=data_list)
    pass


def _get_y_baseline(data_list):
    """
    Get the baseline value of Y axis.

    Parameters
    ----------
    data_list : list
        A one-dimensional list containing numbers.

    Returns
    -------
    y_baseline : int or float
        The smallest value among the numbers in the list and 0.
    """
    list_min_value = min(data_list)
    y_baseline = min(list_min_value, 0)
    return y_baseline

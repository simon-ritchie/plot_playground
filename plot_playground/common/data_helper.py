"""
Module for common function related to data.
"""

from datetime import datetime

import numpy as np


def cast_df_column_to_date_str(df, column_name):
    """
    Convert the column of the data frame to the format of the date
    string (%Y-%m-%d format).

    Parameters
    ----------
    df : DataFrame
        A data frame containing the column to be cast.
    column_name : str or date or datetime-like
        Column name of the date column to cast.
        In the case of a character string, only the format %Y-%m-%d
        is acceptable.

    Returns
    -------
    df : DataFrame
        Data frame after casting.

    Raises
    ------
    ValueError
        - If the target column contains missing values.
        - If it contains a value of date format that is not supported.
    """
    if null_value_exists_in_df(df=df, column_name=column_name):
        err_msg = 'The date column contains a missing value.'
        raise ValueError(err_msg)
    df[column_name] = df[column_name].astype(np.str, copy=False)
    df[column_name] = df[column_name].apply(
        _convert_year_to_date_str
    )
    df[column_name] = df[column_name].apply(
        _convert_month_to_date_str
    )
    date_str_list = df[column_name].tolist()
    for i, date_str in enumerate(date_str_list):
        date_str = date_str[:10]
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except Exception:
            err_msg = 'It contains a value in the form of an unsupported date: %s' \
                % date_str
            raise ValueError(err_msg)
        date_str_list[i] = date_str
    df[column_name] = date_str_list
    return df


def _convert_month_to_date_str(month_str):
    """
    Convert string of month format to date format. If it is not a month
    format, return the value without converting.

    Parameters
    ----------
    month_str : str
        String to be converted. e.g., 2019-01

    Returns
    -------
    date_str : str
        String converted to date format. e.g., 2019-01-01
    """
    if len(month_str) != 7:
        return month_str
    date_str = month_str + '-01'
    return date_str


def _convert_year_to_date_str(year_str):
    """
    Convert string of year format to date format. If it is not a year
    format, return the value without converting.

    Parameters
    ----------
    year_str : str
        String to be converted. e.g., 2019

    Returns
    -------
    date_str : str
        String converted to date format. e.g., 2019-01-01
    """
    if len(year_str) != 4:
        return year_str
    date_str = year_str + '-01-01'
    return date_str


def null_value_exists_in_df(df, column_name):
    """
    Get a boolean value as to whether a missing value is included
    in a specific column of the data frame.

    Parameters
    ----------
    df : DataFrame
        Data frame to be checked.
    column_name : str
        The column to be checked.

    Returns
    -------
    result : bool
        If missing values ​​are included, True is set.
    """
    if df[column_name].isnull().any():
        return True
    return False


def validate_null_value_not_exists_in_df(df, columns):
    """
    Check that missing values ​​do not exist in the list of
    target columns.

    Parameters
    ----------
    df : DataFrame
        Data frame to be checked.
    columns : array-like
        A list of column names to be checked.

    Raises
    ------
    ValueError
        If there is a column containing missing values.
    """
    for column_name in columns:
        null_value_exists = null_value_exists_in_df(
            df=df, column_name=column_name)
        if not null_value_exists:
            continue
        err_msg = 'A missing value is included in the data frame.'
        err_msg += '\ncolumn name: %s' % column_name
        raise ValueError(err_msg)


NUMERIC_CLASS_TUPLE = (
    int,
    float,
    np.int,
    np.int8,
    np.int16,
    np.int32,
    np.int64,
    np.uint,
    np.uint8,
    np.uint16,
    np.uint32,
    np.uint64,
    np.float,
    np.float16,
    np.float32,
    np.float64,
)


def is_numeric_value(value):
    """
    Get a boolean on whether the target value is a number.

    Parameters
    ----------
    value : *
        The value to be checked.

    Returns
    -------
    result : bool
        If the value is a numeric value of Python or NumPy,
        it is set to True. For other types, for example str
        or bool, False is set.
    """
    if isinstance(value, bool):
        return False
    if isinstance(value, NUMERIC_CLASS_TUPLE):
        return True
    return False


def validate_all_values_are_numeric(df, columns):
    """
    Check that the value of the target column is all numeric.

    Parameters
    ----------
    df : DataFrame
        Data frame to be checked.
    columns : array-like
        A list of column names to be checked.

    Raises
    ------
    ValueError
        If there are non-numeric values.
    """
    for column_name in columns:
        value_list = df[column_name].tolist()
        for value in value_list:
            if is_numeric_value(value=value):
                continue
            err_msg = 'There are values ​​that are not numeric.'
            err_msg += '\ncolumn name: %s' % column_name
            err_msg += '\nvalue type: %s' % type(value)
            raise ValueError(err_msg)


def get_year_str_from_date_str(date_str):
    """
    Get the year string from the date string.

    Parameters
    ----------
    date_str : str
        A string of dates. e.g., '2019-01-01'.

    Returns
    -------
    year_str : str
        A string of years. e.g., '2019'.
    """
    year_str = date_str[:4]
    return year_str


def get_df_min_value(df, columns):
    """
    Get the minimum value in the designated column of the data frame.

    Parameters
    ----------
    df : DataFrame
        The target data frame.
    columns : array-like
        A list of columns to be calculated.

    Returns
    -------
    min_value : int or float
        The calculated minimum value.
    """
    min_value = df.loc[:, columns].min().min()
    return min_value


def get_df_max_value(df, columns):
    """
    Get the maximum value in the designated column of the data frame.

    Parameters
    ----------
    df : DataFrame
        The target data frame.
    columns : array-like
        A list of columns to be calculated.

    Returns
    -------
    max_value : int or float
        The calculated maximum value.
    """
    max_value = df.loc[:, columns].max().max()
    return max_value


def convert_numpy_val_to_python_val(value):
    """
    Convert NumPy type value to Python type value.

    Parameters
    ----------
    value : *
        The value to be converted.

    Returns
    -------
    value : *
        The converted value.
    """
    np_int_types = (
        np.int,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.uint,
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
    )
    if isinstance(value, np_int_types):
        return int(value)
    np_float_types = (
        np.float,
        np.float16,
        np.float32,
        np.float64,
    )
    if isinstance(value, np_float_types):
        return float(value)
    return value


def convert_dict_or_list_numpy_val_to_python_val(target_obj):
    """
    Converts the value of NumPy type in dictionary or list into
    Python type value.

    Parameters
    ----------
    target_obj : dict or list
        Dictionary or list to be converted.

    Returns
    -------
    target_obj : dict or list
        Dictionary or list after conversion.

    Raises
    ------
    ValueError
        If dictionaries and lists are specified.
    """
    if isinstance(target_obj, dict):
        for key, value in target_obj.items():
            if isinstance(value, (dict, list)):
                target_obj[key] = convert_dict_or_list_numpy_val_to_python_val(
                    target_obj=value
                )
                continue
            target_obj[key] = convert_numpy_val_to_python_val(
                value=value)
            continue
        return target_obj
    if isinstance(target_obj, list):
        for i, value in enumerate(target_obj):
            if isinstance(value, (dict, list)):
                target_obj[i] = convert_dict_or_list_numpy_val_to_python_val(
                    target_obj=value
                )
                continue
            target_obj[i] = convert_numpy_val_to_python_val(value=value)
            continue
        return target_obj
    err_msg = 'A type that is not a dictionary or list is specified: %s' \
        % type(target_obj)
    raise ValueError(err_msg)

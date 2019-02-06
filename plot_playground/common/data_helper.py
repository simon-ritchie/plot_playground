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
    if df[column_name].isnull().any():
        err_msg = 'The date column contains a missing value.'
        raise ValueError(err_msg)
    df[column_name] = df[column_name].astype(np.str, copy=False)
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

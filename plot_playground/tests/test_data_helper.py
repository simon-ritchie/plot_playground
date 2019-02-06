"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_data_helper --skip_jupyter 1
"""

from nose.tools import assert_equal, assert_true, assert_raises, assert_false
import pandas as pd

from plot_playground.common import data_helper


def test_cast_df_column_to_date_str():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_cast_df_column_to_date_str --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'date': None,
    }])
    kwargs = {
        'df': df,
        'column_name': 'date',
    }
    assert_raises(
        ValueError,
        data_helper.cast_df_column_to_date_str,
        **kwargs
    )

    df = pd.DataFrame(data=[{
        'date': '19700101',
    }])
    kwargs = {
        'df': df,
        'column_name': 'date',
    }
    assert_raises(
        ValueError,
        data_helper.cast_df_column_to_date_str,
        **kwargs
    )

    df = pd.DataFrame(data=[{
        'date': '1970-01-01 10:00:00',
    }])
    data_helper.cast_df_column_to_date_str(
        df=df, column_name='date')
    assert_equal(
        df.loc[0, 'date'], '1970-01-01'
    )


def test_null_value_exists_in_df():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_null_value_exists_in_df --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'a': None,
        'b': 100,
    }])

    result = data_helper.null_value_exists_in_df(
        df=df, column_name='a')
    assert_true(result)

    result = data_helper.null_value_exists_in_df(
        df=df, column_name='b')
    assert_false(result)

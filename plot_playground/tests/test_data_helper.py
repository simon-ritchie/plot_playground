"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_data_helper --skip_jupyter 1
"""

from nose.tools import assert_equal, assert_true, assert_raises, assert_false
import pandas as pd
import numpy as np

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


def test_validate_null_value_not_exists_in_df():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_validate_null_value_not_exists_in_df --skip_jupyter 1
    """

    df = pd.DataFrame(data=[{
        'a': 100,
        'b': None,
        'c': 200,
    }])
    kwargs = {
        'df': df,
        'columns': ['a', 'b'],
    }
    assert_raises(
        ValueError,
        data_helper.validate_null_value_not_exists_in_df,
        **kwargs
    )

    data_helper.validate_null_value_not_exists_in_df(
        df=df, columns=['a', 'c'])


def test_is_numeric_value():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_is_numeric_value --skip_jupyter 1
    """
    result = data_helper.is_numeric_value(value=100)
    assert_true(result)
    result = data_helper.is_numeric_value(value=1.5)
    assert_true(result)
    result = data_helper.is_numeric_value(value=np.int(100))
    assert_true(result)

    result = data_helper.is_numeric_value(value='apple')
    assert_false(result)
    result = data_helper.is_numeric_value(value=True)
    assert_false(result)


def test_validate_all_values_are_numeric():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_validate_all_values_are_numeric --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'a': 100,
        'b': 'apple',
    }, {
        'a': 100.5,
        'b': 'orange',
    }])
    kwargs = {
        'df': df,
        'columns': ['a', 'b'],
    }
    assert_raises(
        ValueError,
        data_helper.validate_all_values_are_numeric,
        **kwargs
    )

    data_helper.validate_all_values_are_numeric(
        df=df, columns=['a'])


def test_get_year_str_from_date_str():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_get_year_str_from_date_str --skip_jupyter 1
    """
    year_str = data_helper.get_year_str_from_date_str(
        date_str='1970-01-01')
    assert_equal(year_str, '1970')


def test_get_df_min_value():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_get_df_min_value --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'a': 100,
        'b': 200,
        'c': 300,
    }, {
        'a': 50,
        'b': 30,
        'c': 80,
    }])
    min_value = data_helper.get_df_min_value(df=df, columns=['a', 'c'])
    assert_equal(min_value, 50)

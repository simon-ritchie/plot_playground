"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_data_helper --skip_jupyter 1
"""

from nose.tools import assert_equal, assert_true, assert_raises, assert_false
import pandas as pd
import numpy as np
from voluptuous import Schema, All, Any

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


def test_get_df_max_value():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_get_df_max_value --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'a': 100,
        'b': 200,
        'c': 300,
    }, {
        'a': 50,
        'b': 350,
        'c': 80,
    }])
    max_value = data_helper.get_df_max_value(
        df=df, columns=['a', 'c'])
    assert_equal(max_value, 300)


def test_convert_numpy_val_to_python_val():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_convert_numpy_val_to_python_val --skip_jupyter 1
    """
    value = data_helper.convert_numpy_val_to_python_val(value=np.int64(100))
    assert_true(isinstance(value, int))

    value = data_helper.convert_numpy_val_to_python_val(value=np.float16(0.5))
    assert_true(isinstance(value, float))

    value = data_helper.convert_numpy_val_to_python_val(value='apple')
    assert_true(isinstance(value, str))


def test_convert_dict_or_list_numpy_val_to_python_val():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test_convert_dict_or_list_numpy_val_to_python_val --skip_jupyter 1
    """
    target_obj = {
        'a': {'b': {'c': np.int64(100)}},
        'd': [np.int16(200)],
        'e': np.float16(0.5),
        'f': 'apple',
    }
    target_obj = data_helper.convert_dict_or_list_numpy_val_to_python_val(
        target_obj=target_obj)
    schema = Schema(
        schema={
            'a': {'b': {'c': All(int, 100)}},
            'd': [All(int, 200)],
            'e': All(float, 0.5),
            'f': 'apple',
        },
        required=True)
    schema(target_obj)


def test__convert_year_to_date_str():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test__convert_year_to_date_str --skip_jupyter 1
    """
    date_str = data_helper._convert_year_to_date_str(
        year_str='1970')
    assert_equal(date_str, '1970-01-01')

    date_str = data_helper._convert_year_to_date_str(
        year_str='1970-01')
    assert_equal(date_str, '1970-01')


def test__convert_month_to_date_str():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_data_helper:test__convert_month_to_date_str --skip_jupyter 1
    """
    date_str = data_helper._convert_month_to_date_str(
        month_str='1970-01')
    assert_equal(date_str, '1970-01-01')

    date_str = data_helper._convert_month_to_date_str(
        month_str='1970-01-01')
    assert_equal(date_str, '1970-01-01')

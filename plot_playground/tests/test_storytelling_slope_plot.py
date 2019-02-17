"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_storytelling_slope_plot
"""

from nose.tools import assert_equal, assert_true, assert_raises
import pandas as pd
from voluptuous import Schema, All, Any

from plot_playground.storytelling import slope_plot


def test__validate_df_columns():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_storytelling_slope_plot:test__validate_df_columns --skip_jupyter 1
    """
    df = pd.DataFrame(
        columns=['a' ,'b', 'c'],
        data=[{
            'a': 'apple',
            'b': 100,
            'c': 150,
        }])
    test_df = df.copy()
    del test_df['a']
    kwargs = {
        'df': test_df,
        'label_column_name': 'a',
        'left_value_column_name': 'b',
        'right_value_column_name': 'c',
    }
    assert_raises(
        ValueError,
        slope_plot._validate_df_columns,
        **kwargs
    )

    test_df = df.copy()
    del test_df['b']
    kwargs['df'] = test_df
    assert_raises(
        ValueError,
        slope_plot._validate_df_columns,
        **kwargs
    )

    test_df = df.copy()
    del test_df['c']
    kwargs['df'] = test_df
    assert_raises(
        ValueError,
        slope_plot._validate_df_columns,
        **kwargs
    )

    test_df = df.copy()
    test_df['b'] = '100'
    kwargs['df'] = test_df
    assert_raises(
        ValueError,
        slope_plot._validate_df_columns,
        **kwargs
    )


def test__make_dataset():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_storytelling_slope_plot:test__make_dataset --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'a': 'apple',
        'b': 100,
        'c': 120,
    }, {
        'a': 'orange',
        'b': 140,
        'c': 160,
    }])
    dataset = slope_plot._make_dataset(
        df=df,
        label_column_name='a',
        left_value_column_name='b',
        right_value_column_name='c')
    assert_equal(len(dataset), 2)
    schema = Schema(
        schema={
            'label': 'apple',
            'left': 100,
            'right': 120,
        },
        required=True)
    schema(dataset[0])
    schema = Schema(
        schema={
            'label': 'orange',
            'left': 140,
            'right': 160,
        },
        required=True)

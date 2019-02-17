"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_storytelling_slope_plot
"""

from nose.tools import assert_equal, assert_true, assert_raises
import pandas as pd

from plot_playground.storytelling import slope_plot


def test__validate_df_columns():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_storytelling_slope_plot:test__validate_df_columns
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

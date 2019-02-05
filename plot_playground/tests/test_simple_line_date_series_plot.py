"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_simple_line_date_series_plot
"""

from nose.tools import assert_equal, assert_true, assert_raises
import pandas as pd

from plot_playground.storytelling import simple_line_date_series_plot


def test__validate_df_columns():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_simple_line_date_series_plot:test__validate_df_columns
    """
    df = pd.DataFrame(columns=['a', 'b', 'c'])

    kwargs = {
        'df': df,
        'date_column': 'd',
        'normal_columns': ['a', 'b'],
        'stands_out_columns': ['c'],
    }
    assert_raises(
        ValueError,
        simple_line_date_series_plot._validate_df_columns,
        **kwargs
    )

    kwargs = {
        'df': df,
        'date_column': 'a',
        'normal_columns': ['d'],
        'stands_out_columns': ['b'],
    }
    assert_raises(
        ValueError,
        simple_line_date_series_plot._validate_df_columns,
        **kwargs
    )

    kwargs = {
        'df': df,
        'date_column': 'a',
        'normal_columns': ['b'],
        'stands_out_columns': ['d'],
    }
    assert_raises(
        ValueError,
        simple_line_date_series_plot._validate_df_columns,
        **kwargs
    )

    simple_line_date_series_plot._validate_df_columns(
        df=df, date_column='a', normal_columns=['b'], stands_out_columns=['c'])

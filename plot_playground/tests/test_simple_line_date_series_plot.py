"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_simple_line_date_series_plot
"""

from nose.tools import assert_equal, assert_true, assert_raises
import pandas as pd
from voluptuous import Schema, Any

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


def test__make_legend_dataset():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_simple_line_date_series_plot:test__make_legend_dataset --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'date': '1970-01-03',
        'a': 100,
        'b': 1000,
    }, {
        'date': '1970-01-02',
        'a': 200,
        'b': 2000,
    }])
    legend_dataset = simple_line_date_series_plot._make_legend_dataset(
        df=df,
        date_column='date',
        normal_columns=['b'],
        stands_out_columns=['a'])
    assert_equal(len(legend_dataset), 2)
    print(legend_dataset)
    schema = Schema(
        schema={
            'key': Any('a', 'b'),
            'value': Any(100, 1000),
        },
        required=True)
    for legend_dataset_dict in legend_dataset:
        schema(legend_dataset_dict)


def test__make_year_str_list():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_simple_line_date_series_plot:test__make_year_str_list --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'date': '1970-01-01',
    }, {
        'date': '1972-03-01',
    }, {
        'date': '1970-05-01',
    }])
    year_str_list = simple_line_date_series_plot._make_year_str_list(
        df=df, date_column='date')
    assert_equal(
        year_str_list,
        ['1970-01-01', '1972-01-01']
    )

"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_storytelling_simple_line_date_series_plot
"""

from nose.tools import assert_equal, assert_true, assert_raises, \
    assert_greater_equal
import pandas as pd
from voluptuous import Schema, Any

from plot_playground.storytelling import simple_line_date_series_plot
from plot_playground.common import jupyter_helper
from plot_playground.common import selenium_helper
from plot_playground.common import img_helper
from plot_playground.common import d3_helper
from plot_playground.common import settings


def teardown():
    selenium_helper.exit_webdriver()
    jupyter_helper.empty_test_ipynb_code_cell()


def test__validate_df_columns():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_storytelling_simple_line_date_series_plot:test__validate_df_columns
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
    $ python run_tests.py --module_name plot_playground.tests.test_storytelling_simple_line_date_series_plot:test__make_legend_dataset --skip_jupyter 1
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
    $ python run_tests.py --module_name plot_playground.tests.test_storytelling_simple_line_date_series_plot:test__make_year_str_list --skip_jupyter 1
    """
    df = pd.DataFrame(data=[{
        'date': '1970-01-05',
    }, {
        'date': '1972-03-01',
    }, {
        'date': '1970-05-01',
    }])
    year_str_list = simple_line_date_series_plot._make_year_str_list(
        df=df, date_column='date')
    assert_equal(
        year_str_list,
        ['1970-01-05', '1972-01-01']
    )


def test_display_plot():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_storytelling_simple_line_date_series_plot:test_display_plot
    """
    source_code = """
from plot_playground.tests.test_storytelling_simple_line_date_series_plot import display_test_plot
display_test_plot()
    """
    jupyter_helper.update_ipynb_test_source_code(
        source_code=source_code)
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code(sleep_seconds=10)
    jupyter_helper.hide_header()
    jupyter_helper.hide_input_cell()
    svg_elem = selenium_helper.driver.find_element_by_id(
        settings.TEST_SVG_ELEM_ID
    )
    selenium_helper.save_target_elem_screenshot(
        target_elem=svg_elem)
    expected_img_path = img_helper.get_test_expected_img_path(
        file_name='simple_line_date_series_plot_display_plot')
    similarity = img_helper.compare_img_hist(
        img_path_1=selenium_helper.DEFAULT_TEST_IMG_PATH,
        img_path_2=expected_img_path)
    assert_greater_equal(similarity, 0.9999)
    selenium_helper.exit_webdriver()

    plot_meta = display_test_plot()
    assert_true(
        isinstance(plot_meta, d3_helper.PlotMeta)
    )


def display_test_plot():
    """
    Display a test plot.

    Returns
    -------
    plot_meta : plot_playground.common.d3_helper.PlotMeta
        An object that stores the metadata of the plot.
    """
    df = pd.DataFrame(data=[{
        'date': '2017-11-03',
        'apple': 100,
        'orange': 140,
    }, {
        'date': '2017-12-03',
        'apple': 90,
        'orange': 85,
    }, {
        'date': '2018-04-03',
        'apple': 120,
        'orange': 170,
    }, {
        'date': '2018-09-03',
        'apple': 110,
        'orange': 180,
    }, {
        'date': '2019-02-01',
        'apple': 90,
        'orange': 150,
    }])
    plot_meta = simple_line_date_series_plot.display_plot(
        df=df,
        date_column='date',
        normal_columns=['apple'],
        stands_out_columns=['orange'],
        title='Time series of fruit prices.',
        description='Orange price keeps stable value in the long term.',
        svg_id=settings.TEST_SVG_ELEM_ID)
    return plot_meta

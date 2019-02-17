"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_storytelling_slope_plot
"""

from nose.tools import assert_equal, assert_true, assert_raises, \
    assert_greater_equal
import pandas as pd
from voluptuous import Schema, All, Any

from plot_playground.storytelling import slope_plot
from plot_playground.common import jupyter_helper
from plot_playground.common import selenium_helper
from plot_playground.common import settings
from plot_playground.common import img_helper
from plot_playground.common import d3_helper


def teardonw():
    jupyter_helper.empty_test_ipynb_code_cell()


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
        right_value_column_name='c',
        standing_out_label_name_list=['orange'])
    assert_equal(len(dataset), 2)
    schema = Schema(
        schema={
            'label': 'apple',
            'left': 100,
            'right': 120,
            'isStandingOutData': 0,
        },
        required=True)
    schema(dataset[0])
    schema = Schema(
        schema={
            'label': 'orange',
            'left': 140,
            'right': 160,
            'isStandingOutData': 1,
        },
        required=True)


def test_display_plot():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_storytelling_slope_plot:test_display_plot
    """
    source_code = """
from plot_playground.tests.test_storytelling_slope_plot import display_test_plot
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
    selenium_helper.save_target_elem_screenshot(target_elem=svg_elem)
    selenium_helper.exit_webdriver()
    expected_img_path = img_helper.get_test_expected_img_path(
        file_name='slope_plot_display_plot')
    similarity = img_helper.compare_img_hist(
        img_path_1=selenium_helper.DEFAULT_TEST_IMG_PATH,
        img_path_2=expected_img_path)
    assert_greater_equal(similarity, 0.99)

    plot_meta = display_test_plot()
    assert_true(isinstance(plot_meta, d3_helper.PlotMeta))


def display_test_plot():
    """
    Display a test plot.

    Returns
    -------
    plot_meta : plot_playground.common.d3_helper.PlotMeta
        An object that stores the metadata of the plot.
    """
    df = pd.DataFrame(data=[{
        'a': 'Apple',
        'b': 1.0,
        'c': 1.2,
    }, {
        'a': 'Orange',
        'b': 1.4,
        'c': 1.1,
    }, {
        'a': 'Peach',
        'b': 2.2,
        'c': 1.6,
    }])
    plot_meta = slope_plot.display_plot(
        df=df,
        label_column_name='a',
        left_value_column_name='b',
        right_value_column_name='c',
        standing_out_label_name_list=['Orange'],
        description='The price of orange has dropped from $1.4 to $1.1.',
        title='Fruit price changes in 2017 and 2018.',
        left_value_prefix='$',
        right_value_prefix='$',
        plot_background_color='#333333',
        svg_id=settings.TEST_SVG_ELEM_ID)
    return plot_meta

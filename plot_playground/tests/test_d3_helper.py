"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_d3_helper
"""

import os
import time

from nose.tools import assert_equal, assert_true, assert_greater_equal, \
    assert_raises, assert_not_equal
import numpy as np

from plot_playground.common import d3_helper
from plot_playground.common import selenium_helper
from plot_playground.common import jupyter_helper
from plot_playground.common import settings
from plot_playground.common import img_helper
from plot_playground.storytelling import simple_line_date_series_plot


def setup():
    driver = selenium_helper.start_webdriver()
    jupyter_helper.open_test_jupyter_note_book()


def teardown():
    selenium_helper.exit_webdriver()
    jupyter_helper.empty_test_ipynb_code_cell()


def read_jupyter_test_python_script(script_file_name=None):
    """
    Read the character string of Python script used on
    Jupyter.

    Parameters
    ----------
    script_file_name : str or None, default None
        Filename of the target script (excluding
        the extension).  None is specified only when passing
        through the test runner. Usually, specify a character string.

    Returns
    -------
    script_str : str
        String of loaded script.

    Raises
    ------
    Exception
        If the file not exists.
    """
    if script_file_name is None:
        return ''
    file_path = os.path.join(
        settings.ROOT_DIR,
        'plot_playground',
        'tests',
        'script_on_jupyter',
        '%s.py' % script_file_name
    )
    if not os.path.exists(file_path):
        err_msg = 'Script file not found : %s' \
            % file_path
        raise Exception(err_msg)
    with open(file_path, 'r') as f:
        script_str = str(f.read())
    return script_str


def test_exec_d3_js_script_on_jupyter():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_d3_helper:test_exec_d3_js_script_on_jupyter
    """
    script_str = read_jupyter_test_python_script(
        script_file_name='exec_d3_js_script_on_jupyter')
    jupyter_helper.update_ipynb_test_source_code(
        source_code=script_str)

    jupyter_helper.selenium_helper.driver.refresh()
    time.sleep(3)

    jupyter_helper.run_test_code(sleep_seconds=3)
    driver = selenium_helper.driver
    svg_elem = driver.find_element_by_id(
        settings.TEST_SVG_ELEM_ID
    )
    selenium_helper.save_target_elem_screenshot(
        target_elem=svg_elem)
    expected_img_path = img_helper.get_test_expected_img_path(
        file_name='exec_d3_js_script_on_jupyter')
    similarity = img_helper.compare_img_hist(
        img_path_1=selenium_helper.DEFAULT_TEST_IMG_PATH,
        img_path_2=expected_img_path)
    assert_equal(similarity, 1.0)


def test_make_svg_id():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_d3_helper:test_make_svg_id
    """
    svg_id = d3_helper.make_svg_id()
    assert_true(svg_id.startswith('svg_id_'))
    assert_greater_equal(len(svg_id), 20)


def test_read_template_str():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_d3_helper:test_read_template_str
    """

    kwargs = {
        'template_file_path': 'test_file_not_exists_path/test.csv',
    }
    assert_raises(
        Exception,
        d3_helper.read_template_str,
        **kwargs,
    )

    template_str = d3_helper.read_template_str(
        template_file_path=simple_line_date_series_plot.PATH_CSS_TEMPLATE)
    assert_not_equal(template_str, '')


def test_apply_css_param_to_template():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_d3_helper:test_apply_css_param_to_template
    """
    css_template_str = """
    abc : --test_param_1--px;
    def : --test_param_2--;
    """
    css_param = {
        'test_param_1': 10,
        'test_param_2': "#333333",
    }
    csv_template_str = d3_helper.apply_css_param_to_template(
        css_template_str=css_template_str,
        css_param=css_param
    )
    expected_template_str = """
    abc : 10px;
    def : #333333;
    """
    assert_equal(csv_template_str, expected_template_str)


def test_apply_js_param_to_template():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_d3_helper:test_apply_js_param_to_template
    """
    js_template_str = r"""
    var test_val_1 = {a};
    var test_val_2 = "{b}";
    var test_val_3 = {c};
    var test_val_4 = {d};
    """
    js_param = {
        'a': 100,
        'b': 'apple',
        'c': ['orange'],
        'd': {'lemon': np.int32(200)}
    }
    js_template_str = d3_helper.apply_js_param_to_template(
        js_template_str=js_template_str,
        js_param=js_param)
    expected_js_str = r"""
    var test_val_1 = 100;
    var test_val_2 = "apple";
    var test_val_3 = ["orange"];
    var test_val_4 = {"lemon": 200};
    """
    assert_equal(js_template_str, expected_js_str)


def test_PlotMeta():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_d3_helper:test_PlotMeta
    """
    plot_meta = d3_helper.PlotMeta(
        js_template_str='a',
        js_param={'a': 1},
        css_template_str='b',
        css_param={'b': 2})
    assert_equal(plot_meta.js_template_str, 'a')
    assert_equal(plot_meta.js_param, {'a': 1})
    assert_equal(plot_meta.css_template_str, 'b')
    assert_equal(plot_meta.css_param, {'b': 2})

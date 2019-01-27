"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_selenium_helper
"""

import time

from nose.tools import assert_equal, assert_true, \
    assert_not_equal, assert_false

from plot_playground.common import selenium_helper
from plot_playground.common import jupyter_helper
from plot_playground.tests.test_d3_helper \
    import read_jupyter_test_python_script
from plot_playground.common import settings
from plot_playground.common import img_helper


def teardown():
    selenium_helper.exit_webdriver()
    jupyter_helper.empty_test_ipynb_code_cell()


def test_start_webdriver():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_selenium_helper:test_start_webdriver
    """
    driver = selenium_helper.start_webdriver()
    driver.get('https://www.google.com/')
    assert_equal(
        str(driver.title).lower(),
        'google')


def test_exit_webdriver():
    driver = selenium_helper.start_webdriver()
    assert_not_equal(driver, None)
    selenium_helper.exit_webdriver()
    assert_equal(selenium_helper.driver, None)


def test_chromedriver_process_exists():
    """
    Notes
    -----
    If test this process with selenium running, it will be
    disconnected from the browser and will need to close
    it manually, so will not do such a test pattern.

    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_selenium_helper:test_chromedriver_process_exists
    """
    selenium_helper.kill_chromedriver_process()
    result_bool = selenium_helper.chromedriver_process_exists()
    assert_false(result_bool)


def test_kill_chromedriver_process():
    """
    Notes
    -----
    If test this process with selenium running, it will be
    disconnected from the browser and will need to close
    it manually, so will not do such a test pattern.

    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_selenium_helper:test_kill_chromedriver_process
    """
    selenium_helper.kill_chromedriver_process()
    result_bool = selenium_helper.chromedriver_process_exists()
    assert_false(result_bool)


def test_save_target_elem_screenshot():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_selenium_helper:test_save_target_elem_screenshot
    """

    script_str = read_jupyter_test_python_script(
        script_file_name='exec_d3_js_script_on_jupyter')
    jupyter_helper.update_ipynb_test_source_code(
        source_code=script_str)
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code(sleep_seconds=5)
    driver = selenium_helper.driver
    jupyter_helper.hide_input_cell()
    jupyter_helper.hide_header()
    target_elem = driver.find_element_by_id(
        settings.TEST_SVG_ELEM_ID
    )
    selenium_helper.save_target_elem_screenshot(
        target_elem=target_elem)
    expected_img_path = img_helper.get_test_expected_img_path(
        file_name='exec_d3_js_script_on_jupyter')
    similarity = img_helper.compare_img_hist(
        img_path_1=selenium_helper.DEFAULT_TEST_IMG_PATH,
        img_path_2=expected_img_path)
    assert_equal(similarity, 1.0)

"""
Test command for this module:
$ python run_tests.py --module_name plot_playground.tests.test_selenium_helper
"""

from nose.tools import assert_equal, assert_true, \
    assert_not_equal, assert_false

from plot_playground.common import selenium_helper


def teardown():
    selenium_helper.exit_webdriver()


def test_start_webdriver():
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
    """
    selenium_helper.kill_chromedriver_process()
    result_bool = selenium_helper.chromedriver_process_exists()
    assert_false(result_bool)

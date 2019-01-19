from nose.tools import assert_equal, assert_true, \
    assert_not_equal

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

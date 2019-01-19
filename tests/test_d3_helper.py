from nose.tools import assert_equal, assert_true

from plot_playground.common import d3_helper
from plot_playground.common import selenium_helper


def setup():
    driver = selenium_helper.start_webdriver()


def teardown():
    selenium_helper.exit_webdriver()


def test_1():
    print('test 1')

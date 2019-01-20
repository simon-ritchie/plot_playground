"""
Test command for this module:
$ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper
"""

from nose.tools import assert_equal, assert_true, \
    assert_not_equal, assert_raises, assert_false

from plot_playground.common import jupyter_helper
from plot_playground.common import selenium_helper


def setup():
    selenium_helper.start_webdriver()


def teardown():
    selenium_helper.exit_webdriver()


def test_get_jupyter_root_url_with_token():
    root_url = jupyter_helper.get_jupyter_root_url_with_token()
    assert_true(
        root_url.startswith(jupyter_helper.JUPYTER_ROOT_URL)
    )
    is_in = '?token=' in root_url
    assert_true(is_in)
    selenium_helper.driver.get(root_url)
    is_in = 'home' in str(selenium_helper.driver.title).lower()


def test_get_jupyter_token():
    token_str = jupyter_helper.get_jupyter_token()
    assert_true(
        token_str.startswith('?token='))
    is_space_in = ' ' in token_str
    assert_false(is_space_in)

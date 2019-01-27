"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_img_helper
"""

import os

from nose.tools import assert_equal, assert_true, assert_raises

from plot_playground.common import img_helper
from plot_playground.common import settings


TEST_IMG_PATH_1 = os.path.join(
    settings.ROOT_DIR, 'plot_playground', 'tests', 'test_img_1.png')
TEST_IMG_PATH_2 = os.path.join(
    settings.ROOT_DIR, 'plot_playground', 'tests', 'test_img_2.png')
TEST_IMG_PATH_LIST = [
    TEST_IMG_PATH_1,
    TEST_IMG_PATH_2,
]


def setup():
    _remove_test_img()


def teardown():
    _remove_test_img()


def _remove_test_img():
    """
    Remove the image generated for testing if it exists.
    """
    for test_img_path in TEST_IMG_PATH_LIST:
        if not os.path.exists(test_img_path):
            continue
        os.remove(test_img_path)


def test_assert_img_exists():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_img_helper:test_assert_img_exists
    """
    _remove_test_img()
    assert_raises(
        AssertionError,
        img_helper.assert_img_exists,
        img_path=TEST_IMG_PATH_1)

    open(TEST_IMG_PATH_1, 'a').close()
    img_helper.assert_img_exists(TEST_IMG_PATH_1)
    _remove_test_img()

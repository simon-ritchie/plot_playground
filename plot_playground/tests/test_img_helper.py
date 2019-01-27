"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_img_helper --skip_jupyter 1
"""

import os

from nose.tools import assert_equal, assert_true, assert_raises, \
    assert_less_equal
from PIL import Image

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
    $ python run_tests.py --module_name plot_playground.tests.test_img_helper:test_assert_img_exists --skip_jupyter 1
    """
    _remove_test_img()
    assert_raises(
        AssertionError,
        img_helper.assert_img_exists,
        img_path=TEST_IMG_PATH_1)

    open(TEST_IMG_PATH_1, 'a').close()
    img_helper.assert_img_exists(TEST_IMG_PATH_1)
    _remove_test_img()


def test_compare_img_hist():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_img_helper:test_compare_img_hist --skip_jupyter 1
    """
    _remove_test_img()

    img = Image.new(mode='RGB', size=(50, 50), color='#ff0000')
    img.save(TEST_IMG_PATH_1)
    img.save(TEST_IMG_PATH_2)
    img.close()
    similarity = img_helper.compare_img_hist(
        img_path_1=TEST_IMG_PATH_1,
        img_path_2=TEST_IMG_PATH_2)
    assert_equal(similarity, 1.0)

    img = Image.new(mode='RGB', size=(50, 50), color='#00ff00')
    img.save(TEST_IMG_PATH_2)
    img.close()
    similarity = img_helper.compare_img_hist(
        img_path_1=TEST_IMG_PATH_1,
        img_path_2=TEST_IMG_PATH_2)
    assert_less_equal(similarity, 0.5)

    _remove_test_img()


def test_get_test_expected_img_path():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_img_helper:test_get_test_expected_img_path --skip_jupyter 1
    """
    img_path = img_helper.get_test_expected_img_path(
        file_name='exec_d3_js_script_on_jupyter')
    assert_true(os.path.exists(img_path))

"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper
"""

import os

from nose.tools import assert_equal, assert_true, \
    assert_not_equal, assert_raises, assert_false
from selenium.webdriver.remote.webelement import WebElement

from plot_playground.common import jupyter_helper
from plot_playground.common import selenium_helper


def setup():
    selenium_helper.start_webdriver()


def teardown():
    selenium_helper.exit_webdriver()


def test_get_jupyter_root_url_with_token():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_get_jupyter_root_url_with_token
    """
    root_url = jupyter_helper.get_jupyter_root_url_with_token()
    assert_true(
        root_url.startswith(jupyter_helper.JUPYTER_ROOT_URL)
    )
    is_in = '?token=' in root_url
    assert_true(is_in)
    selenium_helper.driver.get(root_url)
    is_in = 'home' in str(selenium_helper.driver.title).lower()


def test_get_jupyter_token():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_get_jupyter_token
    """
    token_str = jupyter_helper.get_jupyter_token()
    assert_true(
        token_str.startswith('?token='))
    is_space_in = ' ' in token_str
    assert_false(is_space_in)


def test_open_test_jupyter_note_book():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_open_test_jupyter_note_book
    """
    jupyter_helper.open_test_jupyter_note_book()
    assert_equal(
        selenium_helper.driver.title,
        jupyter_helper.TEST_JUPYTER_NOTE_NAME,
        'could not open the Jupyter notebook for testing. Please check that the notebook is properly placed in the target path.'
    )
    selenium_helper.exit_webdriver()


def test__assert_current_page_is_test_notebook():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__assert_current_page_is_test_notebook
    """
    selenium_helper.exit_webdriver()
    assert_raises(
        Exception,
        jupyter_helper._assert_current_page_is_test_notebook
    )

    driver = selenium_helper.start_webdriver()
    driver.get('https://www.google.com/')
    assert_raises(
        Exception,
        jupyter_helper._assert_current_page_is_test_notebook
    )

    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper._assert_current_page_is_test_notebook()


def test__get_test_code_cell_elem():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__get_test_code_cell_elem
    """
    driver = selenium_helper.start_webdriver()
    driver.get('https://www.google.com/')
    assert_raises(
        Exception,
        jupyter_helper._get_test_code_cell_elem
    )

    jupyter_helper.open_test_jupyter_note_book()
    code_cell_elem = jupyter_helper._get_test_code_cell_elem()
    assert_true(
        isinstance(code_cell_elem, WebElement)
    )


def test_TEST_JUPYTER_NOTE_PATH():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_TEST_JUPYTER_NOTE_PATH
    """
    assert_true(
        os.path.exists(jupyter_helper.TEST_JUPYTER_NOTE_PATH)
    )


def test_update_ipynb_test_source_code():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_update_ipynb_test_source_code
    """
    jupyter_helper.update_ipynb_test_source_code(
        source_code='print(100)\nprint(200)')


def test__assert_only_one_code_cell_exists():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__assert_only_one_code_cell_exists
    """
    kwargs = {
        'ipynb_json': {},
    }
    assert_raises(
        AssertionError,
        jupyter_helper._assert_only_one_code_cell_exists,
        **kwargs,
    )

    kwargs = {
        'ipynb_json': {
            'cells': [
                {
                    'cell_type': 'markdown',
                },
            ],
        },
    }
    assert_raises(
        AssertionError,
        jupyter_helper._assert_only_one_code_cell_exists,
        **kwargs
    )

    kwargs = {
        'ipynb_json': {
            'cells': [
                {
                    'cell_type': 'markdown',
                }, {
                    'cell_type': 'code',
                }, {
                    'cell_type': 'code',
                }
            ],
        },
    }
    assert_raises(
        AssertionError,
        jupyter_helper._assert_only_one_code_cell_exists,
        **kwargs
    )

    jupyter_helper._assert_only_one_code_cell_exists(
        ipynb_json={
            'cells': [
                {
                    'cell_type': 'markdown',
                }, {
                    'cell_type': 'code',
                },
            ],
        })


def test__get_ipynb_code_cell_idx():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__get_ipynb_code_cell_idx
    """
    ipynb_json = {
        'cells': [
            {
                'cell_type': 'markdown',
            }, {
                'cell_type': 'code',
            },
        ],
    }
    idx = jupyter_helper._get_ipynb_code_cell_idx(
        ipynb_json=ipynb_json)
    assert_equal(idx, 1)


def test__replace_ipynb_code_cell():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__replace_ipynb_code_cell
    """
    ipynb_json = {
        'cells': [
            {
                'cell_type': 'markdown',
            }, {
                'cell_type': 'code',
                'source': [],
            }
        ]
    }
    source_code = """
print(1)
print(2)
    """
    ipynb_json = jupyter_helper._replace_ipynb_code_cell(
        ipynb_json=ipynb_json,
        source_code=source_code,
        code_cell_idx=1)
    assert_equal(
        ipynb_json['cells'][1]['source'],
        ['print(1)', 'print(2)'])

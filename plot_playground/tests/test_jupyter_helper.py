"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper
"""

import time
import os

from nose.tools import assert_equal, assert_true, \
    assert_not_equal, assert_raises, assert_false
from selenium.webdriver.remote.webelement import WebElement

from plot_playground.common import jupyter_helper
from plot_playground.common import selenium_helper


def setup():
    jupyter_helper.empty_test_ipynb_code_cell


def teardown():
    selenium_helper.exit_webdriver()
    jupyter_helper.empty_test_ipynb_code_cell()


def test_empty_test_ipynb_code_cell():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_empty_test_ipynb_code_cell
    """
    jupyter_helper.update_ipynb_test_source_code(
        source_code='print(1)')
    jupyter_helper.empty_test_ipynb_code_cell()
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code()
    assert_false(
        jupyter_helper.output_text_cell_exists()
    )


def test_output_text_cell_exists():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_output_text_cell_exists
    """
    jupyter_helper.update_ipynb_test_source_code(
        source_code='print(100)')
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code()
    assert_true(jupyter_helper.output_text_cell_exists())
    jupyter_helper.empty_test_ipynb_code_cell()
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code()
    assert_false(jupyter_helper.output_text_cell_exists())


def test_get_jupyter_root_url_with_token():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_get_jupyter_root_url_with_token
    """
    jupyter_helper.selenium_helper.start_webdriver()
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
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code()
    text_output = jupyter_helper.get_test_code_text_output()
    is_in = '100' in text_output
    assert_true(is_in)
    is_in = '200' in text_output
    assert_true(is_in)


def test__assert_only_one_code_cell_exists():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__assert_only_one_code_cell_exists
    """
    kwargs = {
        'ipynb_dict': {},
    }
    assert_raises(
        Exception,
        jupyter_helper._assert_only_one_code_cell_exists,
        **kwargs,
    )

    kwargs = {
        'ipynb_dict': {
            'cells': [
                {
                    'cell_type': 'markdown',
                },
            ],
        },
    }
    assert_raises(
        Exception,
        jupyter_helper._assert_only_one_code_cell_exists,
        **kwargs
    )

    kwargs = {
        'ipynb_dict': {
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
        Exception,
        jupyter_helper._assert_only_one_code_cell_exists,
        **kwargs
    )

    jupyter_helper._assert_only_one_code_cell_exists(
        ipynb_dict={
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
    ipynb_dict = {
        'cells': [
            {
                'cell_type': 'markdown',
            }, {
                'cell_type': 'code',
            },
        ],
    }
    idx = jupyter_helper._get_ipynb_code_cell_idx(
        ipynb_dict=ipynb_dict)
    assert_equal(idx, 1)


def test__replace_ipynb_code_cell():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__replace_ipynb_code_cell
    """
    ipynb_dict = {
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
    ipynb_dict = jupyter_helper._replace_ipynb_code_cell(
        ipynb_dict=ipynb_dict,
        source_code=source_code,
        code_cell_idx=1)
    assert_equal(
        ipynb_dict['cells'][1]['source'],
        ['print(1)\n', 'print(2)\n'])


def test__read_test_ipynb_dict():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__read_test_ipynb_dict
    """
    if not os.path.exists(jupyter_helper.TEST_JUPYTER_NOTE_PATH):
        return
    ipynb_dict = jupyter_helper._read_test_ipynb_dict()
    assert_true(isinstance(ipynb_dict, dict))
    has_key = 'cells' in ipynb_dict
    assert_true(has_key)


def test__save_test_ipynb_dict():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__save_test_ipynb_dict
    """
    jupyter_helper.empty_test_ipynb_code_cell()
    ipynb_dict = jupyter_helper._read_test_ipynb_dict()
    code_cell_idx = jupyter_helper._get_ipynb_code_cell_idx(
        ipynb_dict=ipynb_dict)
    ipynb_dict = jupyter_helper._replace_ipynb_code_cell(
        ipynb_dict=ipynb_dict,
        source_code='print(1)',
        code_cell_idx=code_cell_idx)
    jupyter_helper._save_test_ipynb_dict(ipynb_dict=ipynb_dict)
    ipynb_dict = jupyter_helper._read_test_ipynb_dict()
    assert_equal(
        ipynb_dict['cells'][code_cell_idx]['source'][0],
        'print(1)\n'
    )
    jupyter_helper.empty_test_ipynb_code_cell()


def test_display_cell_menu():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_display_cell_menu
    """
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.display_cell_menu()
    driver = jupyter_helper.selenium_helper.driver
    script = 'return $("#{cell_menu_selector_id_str}").css("display");'.format(
        cell_menu_selector_id_str=jupyter_helper.CELL_MENU_SELECTOR_ID_STR
    )
    display_style = driver.execute_script(script)
    assert_equal(display_style, 'block')


def test_run_test_code():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_run_test_code
    """
    jupyter_helper.update_ipynb_test_source_code(
        source_code='print(1)')
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code()
    text_output = jupyter_helper.get_test_code_text_output()
    assert_equal(text_output, '1')


def test__assert_only_one_output_cell_exists():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test__assert_only_one_output_cell_exists
    """
    jupyter_helper.update_ipynb_test_source_code(
        source_code='print(1)')
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code()
    jupyter_helper._assert_only_one_output_cell_exists()


def test_get_test_code_text_output():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_get_test_code_text_output
    """
    jupyter_helper.update_ipynb_test_source_code(
        source_code='print(100)')
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code()
    text_output = jupyter_helper.get_test_code_text_output()
    assert_equal(text_output, '100')


def test_hide_input_cell():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_hide_input_cell
    """
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.hide_input_cell()
    driver = jupyter_helper.selenium_helper.driver
    script = 'return $(".{input_selector_class_str}").css("display");'.format(
        input_selector_class_str=jupyter_helper.INPUT_SELECTOR_CLASS_STR
    )
    display_style_str = driver.execute_script(script)
    assert_equal(display_style_str, 'none')


def test_hide_header():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_jupyter_helper:test_hide_header
    """
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.hide_header()
    time.sleep(5)
    driver = jupyter_helper.selenium_helper.driver

    script = 'return $("#{header_container_id}").css("display");'.format(
        header_container_id=jupyter_helper.HEADER_CONTAINER_SELECTOR_ID_STR
    )
    display_style_str = driver.execute_script(script)
    assert_equal(display_style_str, 'none')

    script = 'return $("#{menu_bar_container_id}").css("display");'.format(
        menu_bar_container_id=jupyter_helper.\
            MENU_BAR_CONTAINER_SELECTOR_ID_STR
    )
    display_style_str = driver.execute_script(script)
    assert_equal(display_style_str, 'none')

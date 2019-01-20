"""
A module describing Jupyter's general purpose control
function for testing.

Notes
-----
It is necessary to use it with Jupyter running.

See Also
--------
run_tests.py
    Handle startup and shutdown of Jupyter.
"""

import subprocess as sp
import time
import json
import os

from selenium.webdriver.common.keys import Keys

from plot_playground.common import settings
from plot_playground.common import selenium_helper

JUPYTER_ROOT_URL = 'http://localhost:{jupyter_test_port}/'.format(
    jupyter_test_port=settings.JUPYTER_TEST_PORT
)


def get_jupyter_root_url_with_token():
    """
    Get root URL of Jupyter's local server including
    token.

    Returns
    -------
    root_url : str
        The root URL of the target Jupyter.

    Raises
    ------
    Exception
        If Jupyter is not running.
    """
    token_str = get_jupyter_token()
    root_url = JUPYTER_ROOT_URL + token_str
    return root_url


def get_jupyter_token():
    """
    Get the token string of Jupyter for testing.

    Returns
    -------
    token_str : str
        A string of token including the parameter part of
        "?token=".

    Raises
    ------
    Exception
        If Jupyter is not running.
    """
    out = sp.check_output(
        ['jupyter', 'notebook', 'list'])
    out = str(out)
    is_in = JUPYTER_ROOT_URL in out
    if not is_in:
        raise Exception("Jupyter's local server is not running. Please check whether it is started normally in the run_tests.py module.")
    token_str = out.split(JUPYTER_ROOT_URL)[1]
    token_str = token_str.split(' :: ')[0]
    return token_str


TEST_JUPYTER_NOTE_NAME = 'test_on_jupyter'
TEST_JUPYTER_NOTE_URL = "http://localhost:{jupyter_test_port}/notebooks/plot_playground/tests/notes/{test_jupyter_note_name}.ipynb".format(
    jupyter_test_port=settings.JUPYTER_TEST_PORT,
    test_jupyter_note_name=TEST_JUPYTER_NOTE_NAME
)
TEST_JUPYTER_NOTE_PATH = os.path.join(
    settings.ROOT_DIR,
    'tests',
    'notes',
    TEST_JUPYTER_NOTE_NAME + '.ipynb',
)


def open_test_jupyter_note_book():
    """
    Open the Jupyter notebook for testing.

    Raises
    ------
    Exception
        If Jupyter is not running.

    Notes
    -----
    If the note does not exist in the target path for some
    reason, add a test notebook to the following path
    beforehand and place only one code cell.

    plot_playground/tests/notes/test_on_jupyter.ipynb
    """
    driver = selenium_helper.start_webdriver()
    root_url = get_jupyter_root_url_with_token()
    driver.get(root_url)
    test_note_url = TEST_JUPYTER_NOTE_URL
    driver.get(test_note_url)
    loop_count = 0
    while loop_count < 10:
        if driver.title == TEST_JUPYTER_NOTE_NAME:
            break
        loop_count += 1
        time.sleep(1)


def get_jupyter_test_code_output_text():
    """
    Get the character string of the output after the
    test cell execution.

    Returns
    -------
    output_text : str
        The character string of the output.

    Raises
    ------
    Exception
        - If Jupyter is not running.
        - If the test notebook is not open.
        - If output cell does not exist.
        - If there are multiple output cells.
    """
    _assert_current_page_is_test_notebook()
    text_output_elem = _get_test_code_text_output_elem()
    pass


def update_ipynb_test_source_code(source_code):
    """
    Directly update code in JSON of the ipynb file.
    It is difficult to control Jupyter's input to the
    cell via selenium, so use this function.

    Parameters
    ----------
    source_code : str
        Source code to set.
    """
    source_list = source_code.split('\n')
    with open(TEST_JUPYTER_NOTE_PATH, 'r') as f:
        ipynb_json = json.load(f)
    print('json', ipynb_json)
    # _assert_code_cell_exists(ipyn)


def _get_test_code_cell_elem():
    """
    Get the WebElement of the form to be used as a test
    code cell.

    Raises
    ------
    Exception
        - If the Jupyter code cell does not exist on the
            current page.
        - If there are multiple cells of code.

    Returns
    -------
    code_cell_elem : selenium.webdriver.remote.webelement.WebElement
        WebElement of code input form.
    """
    _assert_current_page_is_test_notebook()
    code_cell_elem_list = selenium_helper.driver.find_elements_by_css_selector(
        'div.CodeMirror.cm-s-ipython')
    if len(code_cell_elem_list) == 0:
        raise Exception('Could not find any cell for code input. Please check if Jupyter structure has changed.')
    if len(code_cell_elem_list) != 1:
        raise Exception('There are several input cells on the test notebook. Please adjust to only one.')
    code_cell_elem = code_cell_elem_list[0]
    return code_cell_elem


def _assert_current_page_is_test_notebook():
    """
    Check that the page currently open in selenium is a Jupyter
    notebook for testing.

    Raises
    ------
    Exception
        - If webdriver is not running.
        - If the test notebook is not open.
    """
    if selenium_helper.driver is None:
        raise Exception('Webdriver is not running.')
    if selenium_helper.driver.title != TEST_JUPYTER_NOTE_NAME:
        raise Exception('The test notebook is not open.')

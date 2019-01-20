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
    token_str = get_jupyter_token()
    test_note_url = TEST_JUPYTER_NOTE_URL + token_str
    driver.get(test_note_url)

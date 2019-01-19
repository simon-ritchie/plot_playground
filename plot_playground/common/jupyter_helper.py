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
    out = sp.check_output(
        ['jupyter', 'notebook', 'list'])
    out = str(out)
    is_in = JUPYTER_ROOT_URL in out
    if not is_in:
        raise Exception("Jupyter's local server is not running. Please check whether it is started normally in the run_tests.py module.")
    token_str = out.split(JUPYTER_ROOT_URL)[1]
    token_str = token_str.split(' :: ')[0]
    root_url = JUPYTER_ROOT_URL + token_str
    return root_url

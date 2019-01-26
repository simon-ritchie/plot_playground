"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_d3_helper
"""

import os
import time

from nose.tools import assert_equal, assert_true

from plot_playground.common import d3_helper
from plot_playground.common import selenium_helper
from plot_playground.common import jupyter_helper
from plot_playground.common import settings


def setup():
    driver = selenium_helper.start_webdriver()
    jupyter_helper.open_test_jupyter_note_book()


def teardown():
    selenium_helper.exit_webdriver()
    jupyter_helper.empty_test_ipynb_code_cell()


def read_jupyter_test_python_script(script_file_name):
    """
    Read the character string of Python script used on
    Jupyter.

    Parameters
    ----------
    script_file_name : str
        Filename of the target script (excluding
        the extension).

    Returns
    -------
    script_str : str
        String of loaded script.

    Raises
    ------
    Exception
        If the file not exists.
    """
    file_path = os.path.join(
        settings.ROOT_DIR,
        'plot_playground',
        'tests',
        'script_on_jupyter',
        '%s.py' % script_file_name
    )
    if not os.path.exists(file_path):
        err_msg = 'Script file not found : %s' \
            % file_path
        raise Exception(err_msg)
    with open(file_path, 'r') as f:
        script_str = str(f.read())
    return script_str


def test_exec_d3_js_script_on_jupyter():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_d3_helper:test_exec_d3_js_script_on_jupyter
    """
    script_str = read_jupyter_test_python_script(
        script_file_name='exec_d3_js_script_on_jupyter')
    jupyter_helper.update_ipynb_test_source_code(
        source_code=script_str)

    jupyter_helper.selenium_helper.driver.refresh()
    time.sleep(3)

    jupyter_helper.run_test_code(sleep_seconds=3)
    pass


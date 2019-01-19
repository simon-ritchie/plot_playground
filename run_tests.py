"""
Module for test execution. Since it also includes
confirmation of display of D3.js, commands for
starting Jupyter in another process are also executed.
"""

import os
import sys
import time
import multiprocessing as mp
import subprocess as sp

sys.path.append('./plot_playground/')
from common.settings import JUPYTER_TEST_PORT


def run_jupyter_process():
    """
    Start Jupyter process for testing.
    """
    os.system(
        'jupyter notebook --no-browser --port={jupyter_test_port} &'.format(
            jupyter_test_port=JUPYTER_TEST_PORT
        ))


def is_jupyter_started():
    """
    Get the boolean value as to whether Jupyter for testing has
    been started or not.

    Returns
    -------
    result : bool
        If it is started this function will returns True.
    """
    out = sp.check_output(
        ['jupyter', 'notebook', 'list'])
    out = str(out)
    is_in = str(JUPYTER_TEST_PORT) in out
    if is_in:
        return True
    return False


def stop_jupyter():
    """
    Stop Jupyter of the port number used in the test.
    """
    os.system('jupyter notebook stop {jupyter_test_port}'.format(
        jupyter_test_port=JUPYTER_TEST_PORT
    ))


if __name__ == '__main__':
    stop_jupyter()
    jupyter_process = mp.Process(target=run_jupyter_process)
    jupyter_process.start()

    os.system('python setup.py install')
    while not is_jupyter_started():
        time.sleep(1)
    os.system('nosetests -s')
    stop_jupyter()
    jupyter_process.terminate()
    os.system('taskkill /im chromedriver.exe /f')

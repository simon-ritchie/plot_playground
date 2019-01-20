"""
Module for test execution. Since it also includes
confirmation of display of D3.js, commands for
starting Jupyter in another process are also executed.

Notes
-----
Currently, since each command is assumed to be in the
Windows environment, it is necessary to carry out the
test also in the Windows environment.
"""

import argparse
import os
import sys
import time
import multiprocessing as mp
import subprocess as sp
import xml.etree.ElementTree as ET
from datetime import datetime

from win10toast import ToastNotifier
import nose

sys.path.append('./plot_playground/')
from common.settings import JUPYTER_TEST_PORT
from common import selenium_helper


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


def run_nose_command(module_name):
    """
    Execute the test command with the Nose library, and
    obtain the number of execution tests and the number of
    failure tests.

    Parameters
    ----------
    module_name : str
        Name of the module to be tested. Specify in a form
        including a path. Omit extension specification.
        If an empty character is specified, all tests are
        targeted.

    Returns
    -------
    test_num : int
        Number of tests executed.
    failure_num : int
        Number of failed tests.
    """
    xml_path = 'log_test.xml'
    nose_command = 'nosetests'
    if module_name != '':
        nose_command += ' %s' % module_name
    nose_command += ' -s --with-xunit --xunit-file={xml_path}'.format(
        xml_path=xml_path
    )
    nose_output = sp.check_output(
        nose_command,
        shell=True)
    with open(xml_path, 'r') as f:
        test_xml = f.read()
        xml_root_elem = ET.fromstring(text=test_xml)
    test_num = int(xml_root_elem.attrib['tests'])
    failure_num = int(xml_root_elem.attrib['failures'])
    return test_num, failure_num


if __name__ == '__main__':
    command_description = 'Command to execute the defined test.'
    parser = argparse.ArgumentParser(
        description=command_description)
    parser.add_argument(
        '--module_name',
        default='',
        help='The specific module name to be tested. Extension names are not included. It must be specified as a character string containing a path. If omitted, all modules are subject to test execution.')
    args = parser.parse_args()
    module_name = args.module_name

    stop_jupyter()
    jupyter_process = mp.Process(target=run_jupyter_process)
    jupyter_process.start()

    os.system('python setup.py install')
    while not is_jupyter_started():
        time.sleep(1)

    test_num, failure_num = run_nose_command(
        module_name=module_name)

    stop_jupyter()
    jupyter_process.terminate()
    selenium_helper.kill_chromedriver_process()

    toast_msg = '----------------------------'
    toast_msg += '\n%s' % datetime.now()
    toast_msg += '\ntest num: %s' % test_num
    toast_msg += '\nfailure num: %s' % failure_num
    toast_msg += '\n----------------------------'
    toast_notifier = ToastNotifier()
    toast_notifier.show_toast(
        title='The test is completed.',
        msg=toast_msg,
        duration=30)

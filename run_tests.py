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


LOG_FILE_PATH_FAILED_INFO = 'log_failed_test.log'
LOG_FILE_PATH_TEST_INFO = 'log_test.xml'


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
    error_num : int
        Number of errors.
    failures_num : int
        Number of tests failed.

    Notes
    -----
    The nose test process is divided by module. Similar processing
    is also provided by nose argument (e.g., --with-isolation),
    but since error occurs, it is divided manually.
    """
    _remove_failed_info_log_file()

    if module_name != '':
        target_module_list = [module_name]
    else:
        target_module_list = _get_overall_module_list()

    xml_path = LOG_FILE_PATH_TEST_INFO
    test_num = 0
    error_num = 0
    failures_num = 0
    for module_name in target_module_list:
        nose_command = 'nosetests'
        nose_command += ' %s' % module_name
        nose_command += ' --with-xunit --xunit-file={xml_path} -s -v'.format(
            xml_path=xml_path
        )
        print('nose command: %s' % nose_command)
        os.system(nose_command)
        with open(xml_path, 'r') as f:
            test_xml = f.read()
            xml_root_elem = ET.fromstring(text=test_xml)
        test_num += int(xml_root_elem.attrib['tests'])
        error_num += int(xml_root_elem.attrib['errors'])
        failures_num += int(xml_root_elem.attrib['failures'])
        if (error_num != 0 or failures_num != 0):
            _append_failed_info()
    _print_test_result(
        test_num=test_num, error_num=error_num,
        failures_num=failures_num)
    return test_num, error_num, failures_num


def _print_test_result(test_num, error_num, failures_num):
    """
    Output the test result to the console.

    Parameters
    ----------
    test_num : int
        Number of tests executed.
    error_num : int
        Number of errors.
    failures_num : int
        Number of tests failed.
    """
    print(
        'test num:', test_num, ', error num:', error_num,
        ', failures num:', failures_num)
    if error_num == 0 and failures_num == 0:
        return
    with open(LOG_FILE_PATH_FAILED_INFO, 'r') as f:
        failed_info = f.read()
        print(failed_info)


def _append_failed_info():
    """
    Add test failure information to the log file.
    """
    error_str_list = []
    with open(LOG_FILE_PATH_TEST_INFO, 'r') as f:
        test_xml = f.read()
        print(test_xml)
        error_splited_str_list = test_xml.split('end captured logging')
        for error_str in error_splited_str_list:
            error_str = error_str.split('begin captured logging')[0]
            if error_str.find('File') == -1:
                continue
            error_str = '\nFile'.join(error_str.split('File')[1:])
            error_str = error_str.replace(' >>', '')
            error_str_list.append(error_str)
    with open(LOG_FILE_PATH_FAILED_INFO, 'a+') as f:
        for error_str in error_str_list:
            f.write(error_str)


def _remove_failed_info_log_file():
    """
    Remove the log file of test failure information.
    """
    if not os.path.exists(LOG_FILE_PATH_FAILED_INFO):
        return
    os.remove(LOG_FILE_PATH_FAILED_INFO)


def _get_overall_module_list():
    """
    Get a list of all module names to be tested.

    Returns
    -------
    module_name_list : list of str
        A list containing module names.
        e.g., 'plot_playground.tests.test_your_module'
    """
    module_name_list = []
    file_name_list = os.listdir('plot_playground/tests/')
    for file_name in file_name_list:
        if not file_name.startswith('test_'):
            continue
        if not file_name.endswith('.py'):
            continue
        file_name = file_name.replace('.py', '')
        module_name = 'plot_playground.tests.%s' % file_name
        module_name_list.append(module_name)
    return module_name_list


if __name__ == '__main__':
    command_description = 'Command to execute the defined test.'
    parser = argparse.ArgumentParser(
        description=command_description)
    parser.add_argument(
        '--module_name',
        default='',
        help='The specific module name to be tested. Extension names are not included. It must be specified as a character string containing a path. If omitted, all modules are subject to test execution.'
    )
    parser.add_argument(
        '--skip_jupyter',
        default=0,
        help='Whether to skip startup of Jupyter. It is skipped by specifying 1. In cases where Jupyter is unnecessary, testing will be completed in a short time.',
    )
    args = parser.parse_args()
    module_name = args.module_name
    skip_jupyter = args.skip_jupyter

    if not skip_jupyter:
        stop_jupyter()
        jupyter_process = mp.Process(target=run_jupyter_process)
        jupyter_process.start()
        while not is_jupyter_started():
            time.sleep(1)

    test_num, error_num, failures_num = run_nose_command(
        module_name=module_name)

    if not skip_jupyter:
        stop_jupyter()
        jupyter_process.terminate()
    selenium_helper.kill_chromedriver_process()

    toast_msg = '----------------------------'
    toast_msg += '\ntest num: %s' % test_num
    toast_msg += '\nerror num: %s' % error_num
    toast_msg += '\nfailures num: %s' % failures_num
    toast_notifier = ToastNotifier()
    toast_notifier.show_toast(
        title='The test is completed.',
        msg=toast_msg,
        duration=3)

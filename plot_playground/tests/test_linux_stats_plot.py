"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot
"""

import os

from nose.tools import assert_equal, assert_true, assert_false

from plot_playground.stats import linux_stats_plot


def test__get_log_file_path():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__get_log_file_path --skip_jupyter 1
    """
    log_file_path = linux_stats_plot._get_log_file_path(
        log_dir_path='./log/')
    assert_true(log_file_path.startswith('./log/'))
    assert_true(log_file_path.endswith('.csv'))


def test__remove_log_file():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__remove_log_file --skip_jupyter 1
    """
    test_file_path = './test.csv'
    with open(test_file_path, 'a+') as f:
        f.write('test')
    linux_stats_plot._remove_log_file(log_file_path=test_file_path)
    assert_false(
        os.path.exists(test_file_path)
    )

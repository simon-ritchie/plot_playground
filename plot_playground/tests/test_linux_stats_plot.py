"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot
"""

from nose.tools import assert_equal, assert_true

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

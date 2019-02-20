"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot
"""

import os

from nose.tools import assert_equal, assert_true, assert_false, \
    assert_greater

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


def test__exec_gpustat_command():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__exec_gpustat_command --skip_jupyter 1

    Notes
    -----
    Since this function depends on the OS and GPU, most of the functions
    are tested manually in each environment.
    """
    pre_bool = linux_stats_plot.is_gpu_stats_disabled
    linux_stats_plot.is_gpu_stats_disabled = True
    command_result = linux_stats_plot._exec_gpustat_command()
    assert_equal(command_result, '')

    linux_stats_plot.is_gpu_stats_disabled = pre_bool


def test__get_gpu_num():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__get_gpu_num --skip_jupyter 1
    """
    pre_func = linux_stats_plot._exec_gpustat_command

    def test_func_1():
        return ''

    linux_stats_plot._exec_gpustat_command = test_func_1
    gpu_num = linux_stats_plot._get_gpu_num()
    assert_equal(gpu_num, 0)

    def test_func_2():
        return 'Error on querying NVIDIA devices. Use --debug flag for details'

    linux_stats_plot._exec_gpustat_command = test_func_2
    gpu_num = linux_stats_plot._get_gpu_num()
    assert_equal(gpu_num, 0)

    def test_func_3():
        return "28cb5cca2ca4  Wed Feb 20 07:04:22 2019\n[0] Tesla K80        | 31'C,   0 % |     0 / 11441 MB |\n"

    linux_stats_plot._exec_gpustat_command = test_func_3
    gpu_num = linux_stats_plot._get_gpu_num()
    assert_equal(gpu_num, 1)

    def test_func_4():
        return "28cb5cca2ca4  Wed Feb 20 07:04:22 2019\n[0] Tesla K80        | 31'C,   0 % |     0 / 11441 MB |\n[1] Tesla K80        | 31'C,   0 % |     0 / 11441 MB |\n"

    linux_stats_plot._exec_gpustat_command = test_func_4
    gpu_num = linux_stats_plot._get_gpu_num()
    assert_equal(gpu_num, 2)

    linux_stats_plot._exec_gpustat_command = pre_func


def test__get_memory_usage():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__get_memory_usage --skip_jupyter 1
    """
    memory_usage = linux_stats_plot._get_memory_usage()
    assert_true(isinstance(memory_usage, int))
    assert_greater(memory_usage, 0)


def test__get_disk_usage():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__get_disk_usage --skip_jupyter 1
    """
    disk_usage_gb = linux_stats_plot._get_disk_usage()
    assert_true(isinstance(disk_usage_gb, float))
    assert_greater(disk_usage_gb, 0)

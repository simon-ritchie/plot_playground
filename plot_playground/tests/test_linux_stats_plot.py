"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot
"""

import os
from collections import deque
import multiprocessing as mp
import time

from nose.tools import assert_equal, assert_true, assert_false, \
    assert_greater
import pandas as pd

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


def test__get_gpustat_line_str_by_gpu_idx():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__get_gpustat_line_str_by_gpu_idx --skip_jupyter 1
    """
    pre_func = linux_stats_plot._exec_gpustat_command

    def test_func():
        return "28cb5cca2ca4  Wed Feb 20 07:04:22 2019\n[0] Tesla K80        | 31'C,   0 % |     0 / 11441 MB |\n[1] Tesla K80        | 31'C,   0 % |     0 / 11441 MB |\n"

    linux_stats_plot._exec_gpustat_command = test_func
    target_line_str = linux_stats_plot._get_gpustat_line_str_by_gpu_idx(
        gpu_idx=1
    )
    assert_equal(
        target_line_str,
        "[1] Tesla K80        | 31'C,   0 % |     0 / 11441 MB |"
    )

    linux_stats_plot._exec_gpustat_command = pre_func


def test__get_gpu_memory_usage():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__get_gpu_memory_usage --skip_jupyter 1
    """
    pre_func = linux_stats_plot._exec_gpustat_command

    def test_func():
        return "28cb5cca2ca4  Wed Feb 20 07:04:22 2019\n[0] Tesla K80        | 31'C,   0 % |    110 / 11441 MB |\n[1] Tesla K80        | 31'C,   0 % |   250 / 11441 MB |\n"

    linux_stats_plot._exec_gpustat_command = test_func
    gpu_memory_usage_mb = linux_stats_plot._get_gpu_memory_usage(
        gpu_idx=0
    )
    assert_equal(gpu_memory_usage_mb, 110)
    gpu_memory_usage_mb = linux_stats_plot._get_gpu_memory_usage(
        gpu_idx=1
    )
    assert_equal(gpu_memory_usage_mb, 250)

    linux_stats_plot._exec_gpustat_command = pre_func


def test__save_csv():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__save_csv --skip_jupyter 1
    """
    log_dir_path = './log_plotplayground_stats/'
    os.makedirs(log_dir_path, exist_ok=True)
    log_file_path = linux_stats_plot._get_log_file_path(
        log_dir_path=log_dir_path)
    linux_stats_plot._remove_log_file(
        log_file_path=log_file_path)
    memory_usage_deque = deque([1, 2, 3], maxlen=3)
    disk_usage_deque = deque([4, 5, 6], maxlen=3)
    gpu_memory_usage_deque_list = [
        deque([5, 6, 7], maxlen=3),
        deque([8, 9, 10], maxlen=3),
    ]
    linux_stats_plot._save_csv(
        memory_usage_deque=memory_usage_deque,
        disk_usage_deque=disk_usage_deque,
        gpu_memory_usage_deque_list=gpu_memory_usage_deque_list,
        log_file_path=log_file_path)
    assert_true(
        os.path.exists(log_file_path)
    )
    df = pd.read_csv(log_file_path)
    assert_equal(len(df), 3)
    assert_equal(
        df[linux_stats_plot._COLUMN_NAME_MEMORY_USAGE].tolist(),
        [1, 2, 3]
    )
    assert_equal(
        df[linux_stats_plot._COLUMN_NAME_DISK_USAGE].tolist(),
        [4, 5, 6]
    )
    gpu_column_name_1 = linux_stats_plot.\
        _COLUMN_NAME_GPU_MEMORY_USAGE_FORMAT.format(gpu_idx=0)
    assert_equal(
        df[gpu_column_name_1].tolist(),
        [5, 6, 7]
    )
    gpu_column_name_2 = linux_stats_plot.\
        _COLUMN_NAME_GPU_MEMORY_USAGE_FORMAT.format(gpu_idx=1)
    assert_equal(
        df[gpu_column_name_2].tolist(),
        [8, 9, 10]
    )

    linux_stats_plot._remove_log_file(
        log_file_path=log_file_path)


def test__start_plot_data_updating():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__start_plot_data_updating --skip_jupyter 1
    """
    log_dir_path = './log_plotplayground_stats/'
    os.makedirs(log_dir_path, exist_ok=True)
    log_file_path = linux_stats_plot._get_log_file_path(
        log_dir_path=log_dir_path)
    linux_stats_plot._remove_log_file(log_file_path=log_file_path)

    pre_disabled_val = linux_stats_plot.is_gpu_stats_disabled
    linux_stats_plot.is_gpu_stats_disabled = False
    process = mp.Process(
        target=linux_stats_plot._start_plot_data_updating,
        kwargs={
            'interval_seconds': 1,
            'buffer_size': 2,
            'log_dir_path': log_dir_path,
        })
    process.deamon = True
    process.start()
    time.sleep(25)
    process.terminate()
    df = pd.read_csv(log_file_path)
    assert_equal(len(df), 2)
    is_in = linux_stats_plot._COLUMN_NAME_MEMORY_USAGE in df.columns
    assert_true(is_in)
    is_in = linux_stats_plot._COLUMN_NAME_DISK_USAGE in df.columns
    assert_true(is_in)

    linux_stats_plot.is_gpu_stats_disabled = pre_disabled_val
    linux_stats_plot._remove_log_file(log_file_path=log_file_path)


def test__exit_if_parent_process_has_died():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__exit_if_parent_process_has_died --skip_jupyter 1
    """
    parent_pid = os.getpid()
    kwargs = {'parent_pid': parent_pid}
    process = mp.Process(
        target=linux_stats_plot._exit_if_parent_process_has_died,
        kwargs=kwargs
    )
    process.start()
    assert_true(process.is_alive())
    process.terminate()

    kwargs['parent_pid'] = -1
    process = mp.Process(
        target=linux_stats_plot._exit_if_parent_process_has_died,
        kwargs=kwargs
    )
    process.start()
    time.sleep(10)
    assert_false(process.is_alive())


def test__fill_deque_by_initial_value():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__fill_deque_by_initial_value --skip_jupyter 1
    """
    buffer_size = 3
    deque_obj = deque([100], maxlen=buffer_size)
    deque_obj = linux_stats_plot._fill_deque_by_initial_value(
        deque_obj=deque_obj,
        initial_value=200,
        buffer_size=buffer_size)
    assert_equal(len(deque_obj), 1)

    deque_obj = deque([], maxlen=buffer_size)
    deque_obj = linux_stats_plot._fill_deque_by_initial_value(
        deque_obj=deque_obj,
        initial_value=200,
        buffer_size=buffer_size
    )
    assert_equal(len(deque_obj), 3)
    for value in deque_obj:
        assert_equal(value, 200)

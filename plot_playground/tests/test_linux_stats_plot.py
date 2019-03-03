"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot
"""

from collections import deque

from nose.tools import assert_equal, assert_true, assert_false, \
    assert_greater, assert_not_equal
import pandas as pd
import psutil
from voluptuous import Schema, All, Any

from plot_playground.stats import linux_stats_plot
from plot_playground.common import jupyter_helper
from plot_playground.common import selenium_helper
from plot_playground.common import img_helper
from plot_playground.common import d3_helper
from plot_playground.common import settings


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


def test__update_gpu_disabled_bool():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__update_gpu_disabled_bool --skip_jupyter 1
    """
    pre_bool = linux_stats_plot.is_gpu_stats_disabled
    pre_func = linux_stats_plot._exec_gpustat_command

    linux_stats_plot.is_gpu_stats_disabled = False

    def raise_error():
        raise Exception()

    linux_stats_plot._exec_gpustat_command = raise_error
    linux_stats_plot._update_gpu_disabled_bool()
    assert_true(linux_stats_plot.is_gpu_stats_disabled)

    def pass_func():
        pass

    linux_stats_plot._exec_gpustat_command = pass_func
    linux_stats_plot.is_gpu_stats_disabled = False
    linux_stats_plot._update_gpu_disabled_bool()
    assert_false(linux_stats_plot.is_gpu_stats_disabled)

    linux_stats_plot.is_gpu_stats_disabled = pre_bool
    linux_stats_plot._exec_gpustat_command = pre_func


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


def test__get_disk_usage():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__get_disk_usage --skip_jupyter 1
    """
    disk_usage_gb = linux_stats_plot._get_disk_usage()
    assert_true(isinstance(disk_usage_gb, float))
    assert_greater(disk_usage_gb, 0)


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


def test__make_dataset():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__make_dataset --skip_jupyter 1
    """
    buffer_size = 300
    memory_usage_deque = deque([100, 200], maxlen=buffer_size)
    disk_usage_deque = deque([10, 20], maxlen=buffer_size)
    gpu_memory_usage_deque_list = [
        deque([300, 400], maxlen=buffer_size),
    ]
    deques = linux_stats_plot.Deques(
        svg_id='abc',
        buffer_size=buffer_size,
        memory_usage_deque=memory_usage_deque,
        disk_usage_deque=disk_usage_deque,
        gpu_memory_usage_deque_list=gpu_memory_usage_deque_list)
    dataset = linux_stats_plot._make_dataset(deques=deques)
    assert_equal(len(dataset), 2)
    gpu_column_name = linux_stats_plot.\
        _COLUMN_NAME_GPU_MEMORY_USAGE_FORMAT.format(gpu_idx=0)
    schema = Schema(
        schema={
            linux_stats_plot._COLUMN_NAME_MEMORY_USAGE: Any(100, 200),
            linux_stats_plot._COLUMN_NAME_DISK_USAGE: Any(10, 20),
            gpu_column_name: Any(300, 400)
        },
        required=True)
    for dataset_dict in dataset:
        schema(dataset_dict)

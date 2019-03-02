"""
Test Command
------------
$ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot
"""

import os
from collections import deque
import multiprocessing as mp
import time
import shutil
import sys

from nose.tools import assert_equal, assert_true, assert_false, \
    assert_greater, assert_not_equal
import pandas as pd
from IPython.display import display, HTML

from plot_playground.stats import linux_stats_plot
from plot_playground.common import jupyter_helper
from plot_playground.common import selenium_helper
from plot_playground.common import img_helper
from plot_playground.common import d3_helper
from plot_playground.common import settings

TMP_TEST_LOG_DIR = './log_plotplayground_stats/test/'


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
    log_dir_path = TMP_TEST_LOG_DIR
    os.makedirs(log_dir_path, exist_ok=True)
    log_file_path = linux_stats_plot._get_log_file_path(
        log_dir_path=log_dir_path)
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
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

    if os.path.exists(log_file_path):
        os.remove(log_file_path)


def test__start_plot_data_updating():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__start_plot_data_updating --skip_jupyter 1
    """
    log_dir_path = TMP_TEST_LOG_DIR
    os.makedirs(log_dir_path, exist_ok=True)
    log_file_path = linux_stats_plot._get_log_file_path(
        log_dir_path=log_dir_path)
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    parent_pid = os.getpid()

    pre_disabled_val = linux_stats_plot.is_gpu_stats_disabled
    linux_stats_plot.is_gpu_stats_disabled = False
    process = mp.Process(
        target=linux_stats_plot._start_plot_data_updating,
        kwargs={
            'interval_seconds': 1,
            'buffer_size': 2,
            'log_dir_path': log_dir_path,
            'parent_pid': parent_pid,
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
    shutil.rmtree(log_dir_path, ignore_errors=True)


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


def _error_func():
    """
    A function to generate an error and to confirm that error contents
    are added to the file.
    """
    linux_stats_plot._set_error_setting(
        log_dir_path=TMP_TEST_LOG_DIR, save_error_to_file=True)
    raise Exception('error test.')


def test__set_error_setting():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__set_error_setting --skip_jupyter 1
    """
    linux_stats_plot._set_error_setting(
        log_dir_path=TMP_TEST_LOG_DIR,
        save_error_to_file=False)
    is_in = 'nose' in str(sys.stderr)
    assert_true(is_in)

    process = mp.Process(target=_error_func)
    process.start()
    process.join()

    error_log_path = os.path.join(
        TMP_TEST_LOG_DIR, linux_stats_plot.ERR_FILE_NAME)
    with open(error_log_path, 'r') as f:
        error_log = f.read()
        assert_not_equal(error_log, '')

    sys.stderr = sys.__stderr__


def test__print_error_if_exists():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test__print_error_if_exists --skip_jupyter 1
    """
    error_log_path = os.path.join(
        TMP_TEST_LOG_DIR, linux_stats_plot.ERR_FILE_NAME)
    if os.path.exists(error_log_path):
        os.remove(error_log_path)
    tmp_stdout_path = os.path.join(TMP_TEST_LOG_DIR, 'tmp.log')
    if os.path.exists(tmp_stdout_path):
        os.remove(tmp_stdout_path)
    os.makedirs(TMP_TEST_LOG_DIR, exist_ok=True)
    sys.stdout = open(tmp_stdout_path, 'w')

    with open(error_log_path, 'w') as f:
        f.write('test error message')
    linux_stats_plot._print_error_if_exists(
        log_dir_path=TMP_TEST_LOG_DIR)
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    with open(tmp_stdout_path, 'r') as f:
        printed_log = f.read()
        is_in = 'test error message' in printed_log
        assert_true(is_in)

    if os.path.exists(tmp_stdout_path):
        os.remove(tmp_stdout_path)


def test_display_plot():
    """
    Test Command
    ------------
    $ python run_tests.py --module_name plot_playground.tests.test_linux_stats_plot:test_display_plot
    """
    source_code = """
from plot_playground.tests.test_linux_stats_plot import display_test_plot
display_test_plot()
    """
    jupyter_helper.update_ipynb_test_source_code(
        source_code=source_code
    )
    jupyter_helper.open_test_jupyter_note_book()
    jupyter_helper.run_test_code(sleep_seconds=10)
    jupyter_helper.hide_header()
    jupyter_helper.hide_input_cell()
    selenium_helper.driver.set_window_size(width=1400, height=1300)
    count = 0
    while True:
        try:
            svg_elem = selenium_helper.driver.find_element_by_id(
                settings.TEST_SVG_ELEM_ID
            )
            break
        except Exception:
            count += 1
            if count > 5:
                break
            time.sleep(3)
            continue
    selenium_helper.save_target_elem_screenshot(
        target_elem=svg_elem)
    expected_img_path = img_helper.get_test_expected_img_path(
        file_name='stats_linux_stats_plot_display_plot')
    similarity = img_helper.compare_img_hist(
        img_path_1=selenium_helper.DEFAULT_TEST_IMG_PATH,
        img_path_2=expected_img_path)
    assert_greater(similarity, 0.8)
    selenium_helper.exit_webdriver()

    plot_meta = display_test_plot()
    assert_true(
        isinstance(plot_meta, d3_helper.PlotMeta)
    )

    jupyter_helper.empty_test_ipynb_code_cell()


def display_test_plot():
    """
    Display a test plot.

    Returns
    -------
    plot_meta : plot_playground.common.d3_helper.PlotMeta
        An object that stores the metadata of the plot.
    """
    linux_stats_plot._is_displayed = False
    plot_meta = linux_stats_plot.display_plot(
        log_dir_path=TMP_TEST_LOG_DIR,
        svg_id=settings.TEST_SVG_ELEM_ID)
    return plot_meta


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

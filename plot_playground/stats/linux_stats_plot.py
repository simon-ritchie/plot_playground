"""
Module that handles monitoring plots such as memory usage, disk size,
GPU memory and so on.

Notes
-----
The following libraries are required.
    - $ pip install psutil==5.5.1
    - $ pip install gpustat==0.5.0
It will not be installed by default as installation time will be long.
Please install it manually when you need to use this plot.
(Prioritizes convenience on time-limited cloud kernel of those
who do not use this plot)

This basically supports only Linux environment such as Ubuntu.
"""

import time
import traceback
import multiprocessing as mp
import subprocess as sp
from collections import deque
import os
import sys
from datetime import datetime

import pandas as pd
import numpy as np

from plot_playground.common import d3_helper
from plot_playground.common import data_helper
from plot_playground.common import js_helper_template_path

try:
    import psutil
except ImportError:
    print(traceback.format_exc())
    err_msg = 'Installation of the psutil module is necessary to use this plot. Consider running the following pip command and please restart the notebook.'
    err_msg += '\n$ pip install psutil==5.5.1'
    raise ImportError(err_msg)

is_gpu_stats_disabled = False

try:
    import gpustat
except ImportError:
    is_gpu_stats_disabled = True
    print(traceback.format_exc())
    info_msg = 'Installation of the gpustat module is required to use this plot. Consider the execution of the following pip command and please restart the notebook.'
    info_msg += '\n$ pip install gpustat==0.5.0'
    info_msg += '\nOr maybe your environment is windows (only linux, like Ubuntu, is supported).'
    info_msg += '\nThe GPU information plot has been disabled.'
    print(info_msg)


INTERVAL_SECONDS = 1
PATH_CSS_TEMPLATE = 'stats/linux_stats_plot.css'
PATH_JS_TEMPLATE = 'stats/linux_stats_plot.js'
_is_displayed = False


def display_plot(
        buffer_size=300,
        log_dir_path='./log_plotplayground_stats/',
        svg_id=''):
    """
    Display plots of memory usage, disk usage, GPU information
    etc on Jupyter. Values ​​are updated at regular intervals.

    Parameters
    ----------
    buffer_size : int, default 600
        Buffer size to handle in the plot.
    log_dir_path : str, default './log_plotplayground_stats/'
        Directory where the log is saved.
    svg_id : str, default ''
        ID to set for SVG element. When an empty value is specified,
        a unique character string is generated and used.

    Notes
    -----
    - In some cloud kernels (e.g., Azure Notebooks), disk usage may
        not be acquired correctly in some cases.
    - Depending on the environment, memory usage and disk usage
        will be somewhat different values.
    - This function can be executed only once after starting
        the kernel.

    Raises
    ------
    Exception
        If this function is executed more than once.

    Returns
    -------
    plot_meta : plot_playground.common.d3_helper.PlotMeta
        An object that stores the metadata of the plot.
    """
    global _is_displayed
    if _is_displayed:
        raise Exception('This function can be executed only once after starting the kernel.')
    _update_gpu_disabled_bool()

    if svg_id == '':
        svg_id = d3_helper.make_svg_id()
    parent_pid = int(os.getpid())
    process = mp.Process(
        target=_start_plot_data_updating,
        kwargs={
            'interval_seconds': INTERVAL_SECONDS,
            'buffer_size': buffer_size,
            'log_dir_path': log_dir_path,
            'parent_pid': parent_pid,
            'save_error_to_file': True,
        })
    process.deamon = True
    process.start()

    log_file_path = _get_log_file_path(log_dir_path=log_dir_path)
    count = 0
    while not os.path.exists(log_file_path):
        count += 1
        if count > 60:
            break
        time.sleep(1)

    css_template_str = d3_helper.read_template_str(
        template_file_path=PATH_CSS_TEMPLATE)
    css_param = {
        'svg_id': svg_id,
    }
    css_template_str = d3_helper.apply_css_param_to_template(
        css_template_str=css_template_str,
        css_param=css_param)

    js_template_str = d3_helper.read_template_str(
        template_file_path=PATH_JS_TEMPLATE)
    gpu_num = _get_gpu_num()
    js_param = {
        'svg_id': svg_id,
        'gpu_num': gpu_num,
        'csv_log_file_path': log_file_path,
        'js_helper_func_get_b_box_width': d3_helper.read_template_str(
            template_file_path=js_helper_template_path.GET_B_BOX_WIDTH),
    }
    js_template_str = d3_helper.apply_js_param_to_template(
        js_template_str=js_template_str,
        js_param=js_param)

    svg_height = 200 * (2 + gpu_num) + 20 * (3 + gpu_num)
    html_str = d3_helper.exec_d3_js_script_on_jupyter(
        js_script=js_template_str,
        css_str=css_template_str,
        svg_id=svg_id,
        svg_width=950,
        svg_height=svg_height,
    )

    time.sleep(3)
    _print_error_if_exists(log_dir_path=log_dir_path)
    _is_displayed = True

    plot_meta = d3_helper.PlotMeta(
        html_str=html_str,
        js_template_str=js_template_str,
        js_param=js_param,
        css_template_str=css_template_str,
        css_param=css_param)
    return plot_meta


def _print_error_if_exists(log_dir_path):
    """
    If content exists in the error log, print that error content
    to the console.

    Parameters
    ----------
    log_dir_path : str
        Directory where the log is saved.
    """
    error_log_path = os.path.join(log_dir_path, ERR_FILE_NAME)
    if not os.path.exists(error_log_path):
        return
    with open(error_log_path, 'r') as f:
        error_log = f.read()
    if error_log == '':
        return
    error_log = '---------------------------\nAn error occurred during processing. Please check the following error contents.\n%s' \
        % error_log
    print(error_log)


def _start_plot_data_updating(
        interval_seconds, buffer_size, log_dir_path, parent_pid,
        save_error_to_file=False):
    """
    Start updating the plot data.

    Parameters
    ----------
    interval_seconds : int
        Update interval in seconds. Note: Since command execution
        time etc. are not considered, it is basically longer than
        this value.
    buffer_size : int
        Buffer size to handle in the plot.
    log_dir_path : str
        Directory where the log is saved.
    parent_pid : int
        The parent process id.
    save_error_to_file : bool, default False
        Boolean value as to whether to save error contents to file.
    """

    os.makedirs(log_dir_path, exist_ok=True)
    _set_error_setting(
        log_dir_path=log_dir_path,
        save_error_to_file=save_error_to_file)
    log_file_path = _get_log_file_path(
        log_dir_path=log_dir_path
    )

    gpu_num = _get_gpu_num()
    memory_usage_deque = deque([], maxlen=buffer_size)
    disk_usage_deque = deque([], maxlen=buffer_size)
    disk_free_size_deque = deque([], maxlen=buffer_size)
    gpu_memory_usage_deque_list = []
    for i in range(gpu_num):
        gpu_memory_usage_deque_list.append(
            deque([], maxlen=buffer_size)
        )
    pre_dt = datetime.now()
    while True:
        _exit_if_parent_process_has_died(parent_pid=parent_pid)

        memory_usage = _get_memory_usage()
        memory_usage_deque = _fill_deque_by_initial_value(
            deque_obj=memory_usage_deque,
            initial_value=memory_usage,
            buffer_size=buffer_size)
        memory_usage_deque.append(memory_usage)
        disk_usage_gb = _get_disk_usage()
        disk_usage_deque = _fill_deque_by_initial_value(
            deque_obj=disk_usage_deque, initial_value=disk_usage_gb,
            buffer_size=buffer_size)
        disk_usage_deque.append(disk_usage_gb)
        for i in range(gpu_num):
            gpu_memory_usage_mb = _get_gpu_memory_usage(gpu_idx=i)
            gpu_memory_usage_deque_list[i] = _fill_deque_by_initial_value(
                deque_obj=gpu_memory_usage_deque_list[i],
                initial_value=gpu_memory_usage_mb,
                buffer_size=buffer_size
            )
            gpu_memory_usage_deque_list[i].append(gpu_memory_usage_mb)
        _save_csv(
            memory_usage_deque=memory_usage_deque,
            disk_usage_deque=disk_usage_deque,
            gpu_memory_usage_deque_list=gpu_memory_usage_deque_list,
            log_file_path=log_file_path
        )

        current_dt = datetime.now()
        timedelta = current_dt - pre_dt
        if timedelta.total_seconds() < 1:
            time.sleep(interval_seconds)
        pre_dt = current_dt


def _update_gpu_disabled_bool():
    """
    Updates the boolean value of whether gpu stats is disabled.
    When Linux environment and gpu stats are installed, and GPU
    can not be detected, True will be set to that boolean.
    """
    global is_gpu_stats_disabled
    try:
        _exec_gpustat_command()
    except Exception:
        is_gpu_stats_disabled = True


ERR_FILE_NAME = 'error.log'


def _set_error_setting(
        log_dir_path, save_error_to_file):
    """
    Function to set output of error.

    Parameters
    ----------
    log_dir_path : str
        Directory where the log is saved.
    save_error_to_file : bool
        Boolean value as to whether to save error contents to file.
    """
    error_log_path = os.path.join(log_dir_path, ERR_FILE_NAME)
    os.makedirs(log_dir_path, exist_ok=True)
    if os.path.exists(error_log_path):
        os.remove(error_log_path)
    if not save_error_to_file:
        return
    sys.stderr = open(error_log_path, "w")


def _fill_deque_by_initial_value(
        deque_obj, initial_value, buffer_size):
    """
    Fill the deque object with the initial value.

    Parameters
    ----------
    deque_obj : collections.deque
        The deque object to add to.
    initial_value : int or float
        Initial value to be referenced.
    buffer_size : int
        Buffer size to handle in the plot.

    Returns
    -------
    deque_obj : collections.deque
        Deque object after adding data.
    """
    if len(deque_obj) != 0:
        return deque_obj
    while len(deque_obj) < buffer_size:
        deque_obj.append(initial_value)
    return deque_obj


def _exit_if_parent_process_has_died(parent_pid):
    """
    If there is no parent process, stop the child process.

    Parameters
    ----------
    parent_pid : int
        The Parent process id.
    """
    is_parent_process_alive = False
    for process in psutil.process_iter():
        process_info_dict = process.as_dict(attrs=['pid'])
        if int(process_info_dict['pid']) == parent_pid:
            is_parent_process_alive = True
            break
    if not is_parent_process_alive:
        sys.exit()


_COLUMN_NAME_MEMORY_USAGE = 'memory usage (MB)'
_COLUMN_NAME_DISK_USAGE = 'disk usage (GB)'
_COLUMN_NAME_GPU_MEMORY_USAGE_FORMAT = 'gpu({gpu_idx}) memory usage (MB)'


def _save_csv(
        memory_usage_deque, disk_usage_deque,
        gpu_memory_usage_deque_list, log_file_path):
    """
    Save the acquired data as a CSV for plotting.

    Parameters
    ----------
    memory_usage_deque : collections.deque
        The deque object containing the memory usage value.
    disk_usage_deque : collections.deque
        The deque object containing the disk usage value.
    gpu_memory_usage_deque_list : list of collections.deque
        A list of deque objects containing memory usage of the GPU.
    log_file_path : str
        The file path of the log.
    """
    df_len = len(memory_usage_deque)
    df = pd.DataFrame(
        columns=[
            _COLUMN_NAME_MEMORY_USAGE,
            _COLUMN_NAME_DISK_USAGE,
        ],
        index=np.arange(0, df_len))
    df[_COLUMN_NAME_MEMORY_USAGE] = memory_usage_deque
    df[_COLUMN_NAME_DISK_USAGE] = disk_usage_deque
    for i, gpu_memory_usage_deque in \
            enumerate(gpu_memory_usage_deque_list):
        column_name = _COLUMN_NAME_GPU_MEMORY_USAGE_FORMAT.format(
            gpu_idx=i
        )
        df[column_name] = gpu_memory_usage_deque
    df.to_csv(log_file_path, index=False, encoding='utf-8')


def _get_gpu_memory_usage(gpu_idx):
    """
    Get the GPU memory usage of the specified index.

    Parameters
    ----------
    gpu_idx : int
        Index of target GPU (starting from zero).

    Returns
    -------
    gpu_memory_usage_mb : int
        GPU memory usage in megabytes.
    """
    target_line_str = _get_gpustat_line_str_by_gpu_idx(
        gpu_idx=gpu_idx
    )
    gpu_memory_str = target_line_str.split('|')[2]
    gpu_memory_str = gpu_memory_str.split('/')[0]
    gpu_memory_str = gpu_memory_str.strip()
    gpu_memory_usage_mb = int(gpu_memory_str)
    return gpu_memory_usage_mb


def _get_gpustat_line_str_by_gpu_idx(gpu_idx):
    """
    Gets the command result string at the specified GPU index.

    Parameters
    ----------
    gpu_idx : int
        Index of target GPU (starting from zero).

    Returns
    -------
    target_line_str
        The command result string at the specified GPU index.
    """
    command_result = _exec_gpustat_command()
    target_line_str = command_result.split('\n')[gpu_idx + 1]
    return target_line_str


def _get_disk_usage():
    """
    Get disk usage.

    Returns
    -------
    disk_usage_gb : float
        Disk usage in gigabytes.
    """
    disk_usage = psutil.disk_usage('./')
    disk_usage_gb = round(disk_usage.used / (1024.0 ** 3), 2)
    return disk_usage_gb


def _get_memory_usage():
    """
    Get current memory usage (rss total).

    Returns
    -------
    memory_usage : int
        Memory consumption in megabytes.
    """
    memory_usage = 0
    for process in psutil.process_iter():
        memory_usage += process.memory_info().rss
    memory_usage = int(memory_usage / 1048576)
    return memory_usage


def _get_gpu_num():
    """
    Get the number of GPUs.

    Returns
    -------
    gpu_num : int
        The number of GPUs. 0 is returned under the following
        conditions.
        - The gpustat library is not installed.
        - In an environment without GPU.
        - Environment such as windows.
    """
    command_result = _exec_gpustat_command()
    if command_result == '':
        return 0
    is_in = 'Error' in command_result
    if is_in:
        return 0
    gpu_num = 0
    splited_command_result = command_result.split('\n')
    for i, unit_line_gpu_str in enumerate(splited_command_result):
        if i == 0:
            # Ignore the heading line.
            continue
        if unit_line_gpu_str == '':
            continue
        gpu_num += 1
    return gpu_num


def _exec_gpustat_command():
    """
    Execute the command of the gpustat library and obtain the result.

    Returns
    -------
    command_result : str
        String of command execution result. The string changes
        under each condition as follows.
        - If gpustat is disabled: An empty character will be returned.
        - If there is no GPU: 'Error on querying NVIDIA devices. Use --debug flag for details'
        - If GPU exists more than one: '28cb5cca2ca4  Wed Feb 20 07:04:22 2019\n[0] Tesla K80        | 31'C,   0 % |     0 / 11441 MB |\n[1] Tesla K80        | 31'C,   0 % |     0 / 11441 MB |\n'
    """
    global is_gpu_stats_disabled
    if is_gpu_stats_disabled:
        return ''
    command_result = sp.check_output('gpustat').decode('utf-8')
    return command_result


def _get_log_file_path(log_dir_path):
    """
    Get the path of the log file.

    Parameters
    ----------
    log_dir_path : str
        Directory where the log is saved.

    Returns
    -------
    log_file_path : str
        The path of the log file.
    """
    log_file_path = os.path.join(
        log_dir_path,
        'log_linux_stats_plot.csv'
    )
    return log_file_path

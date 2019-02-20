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


def display_plot(
        interval_seconds=1, buffer_size=600,
        log_dir_path='./log_plotplayground_stats/'):
    """
    Display plots of memory usage, disk usage, GPU information
    etc on Jupyter. Values ​​are updated at regular intervals.

    Parameters
    ----------
    interval_seconds : int, default 1
        Update interval in seconds.
    buffer_size : int, default 600
        Buffer size to handle in the plot.
    log_dir_path : str, default './log_plotplayground_stats/'
        Directory where the log is saved.
    """
    process = mp.Process(
        target=_start_plot_data_updating,
        kwargs={
            'interval_seconds': interval_seconds,
            'buffer_size': buffer_size,
            'log_dir_path': log_dir_path,
        })
    process.deamon = True
    process.start()


def _start_plot_data_updating(
        interval_seconds, buffer_size, log_dir_path):
    """
    Start updating the plot data.

    Parameters
    ----------
    interval_seconds : int
        Update interval in seconds.
    buffer_size : int
        Buffer size to handle in the plot.
    log_dir_path : str
        Directory where the log is saved.
    """
    os.makedirs(log_dir_path, exist_ok=True)
    log_file_path = _get_log_file_path(
        log_dir_path=log_dir_path
    )
    _remove_log_file(log_file_path=log_file_path)
    gpu_num = _get_gpu_num()
    memory_usage_deque = deque([], maxlen=buffer_size)
    disk_usage_deque = deque([], maxlen=buffer_size)
    disk_free_size_deque = deque([], maxlen=buffer_size)
    # gpu_memory_usage_deque = deque([], maxlen=buffer_size)
    while True:
        time.sleep(interval_seconds)
    pass


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


def _remove_log_file(log_file_path):
    """
    Delete the log file if it exists.

    Parameters
    ----------
    log_file_path : str
        The path of the log file.
    """
    if os.path.exists(log_file_path):
        os.remove(log_file_path)


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
        log_dir_path, 'log_linux_stats_plot.csv'
    )
    return log_file_path

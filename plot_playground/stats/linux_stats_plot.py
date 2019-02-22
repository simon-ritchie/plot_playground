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


def display_plot(
        interval_seconds=1, buffer_size=600,
        log_dir_path='./log_plotplayground_stats/'):
    """
    Display plots of memory usage, disk usage, GPU information
    etc on Jupyter. Values ​​are updated at regular intervals.

    Parameters
    ----------
    interval_seconds : int, default 1
        Update interval in seconds. Note: Since command execution
        time etc. are not considered, it is basically longer than
        this value.
    buffer_size : int, default 600
        Buffer size to handle in the plot.
    log_dir_path : str, default './log_plotplayground_stats/'
        Directory where the log is saved.

    Notes
    -----
    - In some cloud kernels (e.g., Azure Notebooks), disk usage may
        not be acquired correctly in some cases.
    - Depending on the environment, memory usage and disk usage
        will be somewhat different values.
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
    pass


def _start_plot_data_updating(
        interval_seconds, buffer_size, log_dir_path):
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
    gpu_memory_usage_deque_list = []
    for i in range(gpu_num):
        gpu_memory_usage_deque_list.append(
            deque([], maxlen=buffer_size)
        )
    while True:
        memory_usage = _get_memory_usage()
        memory_usage_deque.append(memory_usage)
        disk_usage_gb = _get_disk_usage()
        disk_usage_deque.append(disk_usage_gb)
        for i in range(gpu_num):
            gpu_memory_usage_mb = _get_gpu_memory_usage(gpu_idx=i)
            gpu_memory_usage_deque_list[i].append(gpu_memory_usage_mb)
        _save_csv(
            memory_usage_deque=memory_usage_deque,
            disk_usage_deque=disk_usage_deque,
            gpu_memory_usage_deque_list=gpu_memory_usage_deque_list,
            log_file_path=log_file_path
        )
        time.sleep(interval_seconds)


_COLUMN_NAME_MEMORY_USAGE = 'memory usage (MB)'
_COLUMN_NAME_DISK_USGE = 'disk usage (GB)'
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
            _COLUMN_NAME_DISK_USGE,
        ],
        index=np.arange(0, df_len))
    df[_COLUMN_NAME_MEMORY_USAGE] = memory_usage_deque
    df[_COLUMN_NAME_DISK_USGE] = disk_usage_deque
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

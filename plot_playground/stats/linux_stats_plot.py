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
    memory_usage_deque = deque([], maxlen=buffer_size)
    disk_usage_deque = deque([], maxlen=buffer_size)
    disk_free_size_deque = deque([], maxlen=buffer_size)
    gpu_memory_usage_deque = deque([], maxlen=buffer_size)
    while True:
        time.sleep(interval_seconds)
    pass


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

"""
Module that handles monitoring plots such as memory usage, disk size,
GPU memory and so on.
This basically supports only Linux environment such as Ubuntu.
"""

import traceback
import json
from collections import deque
import os
import sys

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

PATH_CSS_TEMPLATE = 'stats/linux_stats_plot.css'
PATH_JS_TEMPLATE = 'stats/linux_stats_plot.js'
deque_dict = {}


def display_plot(buffer_size=300, svg_id=''):
    """
    Display plots of memory usage, disk usage, GPU information
    etc on Jupyter. Values ​​are updated at regular intervals.

    Parameters
    ----------
    buffer_size : int, default 300
        Buffer size to handle in the plot.
    svg_id : str, default ''
        ID to set for SVG element. When an empty value is specified,
        a unique character string is generated and used.

    Notes
    -----
    - In some cloud kernels (e.g., Azure Notebooks), disk usage may
        not be acquired correctly in some cases.
    - Depending on the environment, memory usage and disk usage
        will be somewhat different values.

    Returns
    -------
    plot_meta : plot_playground.common.d3_helper.PlotMeta
        An object that stores the metadata of the plot.
    """
    _update_gpu_disabled_bool()
    if svg_id == '':
        svg_id = d3_helper.make_svg_id()
    _initialize_deque(svg_id=svg_id, buffer_size=buffer_size)

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

    plot_meta = d3_helper.PlotMeta(
        html_str=html_str,
        js_template_str=js_template_str,
        js_param=js_param,
        css_template_str=css_template_str,
        css_param=css_param)
    return plot_meta


class Deques():

    def __init__(
            self, svg_id, buffer_size, memory_usage_deque,
            disk_usage_deque, gpu_memory_usage_deque_list):
        """
        A class that holds each deque object and metadata.
        The same value as the argument is set to the attribute.

        Parameters
        ----------
        svg_id : str
            ID to set for SVG element.
        buffer_size : int
            Buffer size to handle in the plot.
        memory_usage_deque : collections.deque
            The deque object that holds memory usage.
        disk_usage_deque : collections.deque
            The deque object that holds disk usage.
        gpu_memory_usage_deque_list : list of deque
            List of deque holding GPU memory usage.
        """
        self.svg_id = svg_id
        self.buffer_size = buffer_size
        self.memory_usage_deque = memory_usage_deque
        self.disk_usage_deque = disk_usage_deque
        self.gpu_memory_usage_deque_list = gpu_memory_usage_deque_list


def _initialize_deque(svg_id, buffer_size):
    global deque_dict
    gpu_num = _get_gpu_num()
    memory_usage_deque = deque([], maxlen=buffer_size)
    disk_usage_deque = deque([], maxlen=buffer_size)
    disk_free_size_deque = deque([], maxlen=buffer_size)
    gpu_memory_usage_deque_list = []
    for i in range(gpu_num):
        gpu_memory_usage_deque_list.append(
            deque([], maxlen=buffer_size)
        )
    deques = Deques(
        svg_id=svg_id,
        buffer_size=buffer_size,
        memory_usage_deque=memory_usage_deque,
        disk_usage_deque=disk_usage_deque,
        gpu_memory_usage_deque_list=gpu_memory_usage_deque_list)
    deque_dict[svg_id] = deques


def get_dataset(svg_id):

    global deque_dict
    deques = deque_dict[svg_id]
    gpu_num = _get_gpu_num()

    memory_usage = _get_memory_usage()
    deques.memory_usage_deque = _fill_deque_by_initial_value(
        deque_obj=deques.memory_usage_deque,
        initial_value=memory_usage,
        buffer_size=deques.buffer_size)
    deques.memory_usage_deque.append(memory_usage)

    disk_usage_gb = _get_disk_usage()
    deques.disk_usage_deque = _fill_deque_by_initial_value(
            deque_obj=deques.disk_usage_deque,
            initial_value=disk_usage_gb,
            buffer_size=deques.buffer_size)
    deques.disk_usage_deque.append(disk_usage_gb)

    for i in range(gpu_num):
        gpu_memory_usage_mb = _get_gpu_memory_usage(gpu_idx=i)
        deques.gpu_memory_usage_deque_list[i] = \
            _fill_deque_by_initial_value(
                deque_obj=deques.gpu_memory_usage_deque_list[i],
                initial_value=gpu_memory_usage_mb,
                buffer_size=deques.buffer_size)
        deques.gpu_memory_usage_deque_list[i].append(
            gpu_memory_usage_mb
        )

    dataset = _make_dataset(deques=deques)
    return json.dumps(dataset)


_COLUMN_NAME_MEMORY_USAGE = 'memoryUsage'
_COLUMN_NAME_DISK_USAGE = 'diskUsage'
_COLUMN_NAME_GPU_MEMORY_USAGE_FORMAT = 'gpuMemoryUsage{gpu_idx}'


def _make_dataset(deques):
    """
    Make a datasets to handle on Jupyter.

    Parameters
    ----------
    deques : Deques
        An object that stores data to be referred to.

    Returns
    -------
    dataset : list of dicts
        A multidimensional list dataset.
    """
    data_len = len(deques.memory_usage_deque)
    dataset = []
    gpu_num = _get_gpu_num()
    for i in range(data_len):
        data_dict = {}
        data_dict[_COLUMN_NAME_MEMORY_USAGE] = \
            deques.memory_usage_deque[i]
        data_dict[_COLUMN_NAME_DISK_USAGE] = deques.disk_usage_deque[i]
        for j, gpu_memory_usage_deque in \
                enumerate(deques.gpu_memory_usage_deque_list):
            column_name = _COLUMN_NAME_GPU_MEMORY_USAGE_FORMAT.format(
                gpu_idx=j
            )
            data_dict[column_name] = gpu_memory_usage_deque[i]

        dataset.append(data_dict)
    return dataset


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

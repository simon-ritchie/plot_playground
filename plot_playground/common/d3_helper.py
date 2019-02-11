"""
A D3.js common helper module.

Notes
-----
Js string is using bracket, that conflict python string format.
Therefore, r character is required before quotation.
"""

import os
from datetime import datetime
from random import randint
import json
import re

from IPython.display import display, HTML

from plot_playground.common import settings
from plot_playground.common import data_helper


def read_template_str(template_file_path):
    """
    Read string of template file.

    Parameters
    ----------
    template_file_path : str
        The path of the template file under the template directory.
        e.g., storytelling/simple_line_date_series_plot.css

    Returns
    -------
    template_str
        Loaded template string. The repr function is set.

    Raises
    ------
    Exception
        If the file can not be found.
    """
    file_path = os.path.join(
        settings.ROOT_DIR, 'plot_playground', 'template',
        template_file_path)
    if not os.path.exists(file_path):
        err_msg = 'Template file not found : %s' % file_path
        raise Exception(err_msg)
    with open(file_path, 'r') as f:
        template_str = f.read()
    template_str = re.sub(re.compile('/\*.*?\*/', re.DOTALL) , '', template_str)
    template_str = repr(template_str)[1:-1]
    template_str = template_str.replace('\\n', '\n')
    template_str = template_str.replace('\\\\', '\\')
    return template_str


def apply_css_param_to_template(css_template_str, css_param):
    """
    Apply the parameters to the CSS template.

    Parameters
    ----------
    css_template_str : str
        String of CSS template.
    css_param : dict
        A dictionary that stores parameter name in key and parameter
        in value. Parameter name corresponds to string excluding hyphens
        in template.

    Returns
    -------
    css_template_str : str
        Template string after parameters are reflected.
    """
    for key, value in css_param.items():
        key = '--%s--' % key
        css_template_str = css_template_str.replace(key, str(value))
    return css_template_str


def apply_js_param_to_template(js_template_str, js_param):
    """
    Apply the parameters to the js template.

    Parameters
    ----------
    js_template_str : str
        String of js template.
    js_param : dict
        A dictionary that stores parameter name in key and parameter
        in value. If the parameter is a list or dictionary, it is
        converted to Json format.

    Returns
    -------
    js_template_str : str
        Template string after parameters are reflected.
    """
    for key, value in js_param.items():
        if isinstance(value, (dict, list)):
            value = data_helper.convert_dict_or_list_numpy_val_to_python_val(
                target_obj=value)
            value = json.dumps(value)
        key = r'{' + key + r'}'
        value = str(value)
        js_template_str = js_template_str.replace(key, value)
    return js_template_str


D3_SCRIPT_EXEC_HTML = read_template_str(
    template_file_path='base/d3_exec.html')


def exec_d3_js_script_on_jupyter(
        js_script, css_str, svg_id, svg_width, svg_height):
    """
    Execute the JavaScript code in a form that can access
    D3.js.

    Parameters
    ----------
    js_script : str
        Code of JavaScript to be executed.
    css_str : str
        The CSS string to set.
    svg_id : str
        ID set to SVG. Using this ID as a selector, you can
        access with jQuery or D3.js code.
    svg_width : int
        Width set to SVG in pixels.
    svg_height : int
        Height set to SVG in pixels.
    """
    param_dict = {
        'd3_version': settings.D3_VERSION,
        'svg_id': str(svg_id),
        'svg_width': str(svg_width),
        'svg_height': str(svg_height),
        'js_script': js_script,
        'css_str': css_str,
    }
    html = apply_js_param_to_template(
        js_template_str=D3_SCRIPT_EXEC_HTML,
        js_param=param_dict)
    display(HTML(html))


def make_svg_id():
    """
    Generate unique SVG ID using random number and time stamp.

    Returns
    -------
    svg_id : str
        Generated SVG ID.
    """
    timestamp_str = str(datetime.now().timestamp())
    timestamp_str = timestamp_str.replace('.', '_')
    random_int_str = str(randint(10000, 99999))
    svg_id = 'svg_id_{timestamp_str}_{random_int_str}'.format(
        timestamp_str=timestamp_str,
        random_int_str=random_int_str
    )
    return svg_id


class PlotMeta():

    def __init__(
            self, js_template_str, js_param, css_template_str,
            css_param):
        """
        Class dealing with plot metadata.

        Parameters
        ----------
        js_template_str : str
            JavaScript template string after parameter substitution.
        js_param : dict
            A dictionary storing parameters set in the JavaScript template.
        css_template_str : str
            CSS template string after parameter substitution.
        css_param : dict
            A dictionary storing parameters set in the CSS template.
        """
        self.js_template_str = js_template_str
        self.js_param = js_param
        self.css_template_str = css_template_str
        self.css_param = css_param

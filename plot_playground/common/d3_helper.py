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

from IPython.display import display, HTML

from plot_playground.common import settings


D3_REQUIRE_HTML = r"""
<script>
    requirejs.config({
        paths: {
            'd3': ['https://d3js.org/d3.v{d3_version}.min'],
        },
    });
</script>
""".replace(r'{d3_version}', settings.D3_VERSION)


def load_d3_on_jupyter():
    """
    Load D3.js script on Jupyter, so that it enable to
    access d3 methods.
    """
    display(HTML(D3_REQUIRE_HTML))


D3_SCRIPT_EXEC_HTML = r"""
<style>
    {css_str}
</style>

<svg id="{svg_id}" width="{svg_width}" height="{svg_height}">
</svg>
<script>
    require(['d3'], function(d3) {
        {js_script}
    });
</script>
"""


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
    html = D3_SCRIPT_EXEC_HTML.replace(
        r'{svg_id}', str(svg_id))
    html = html.replace(
        r'{svg_width}', str(svg_width))
    html = html.replace(
        r'{svg_height}', str(svg_height))
    html = html.replace(
        r'{js_script}', js_script)
    html = html.replace(
        r'{css_str}', css_str)
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
    template_str = repr(template_str)
    return template_str

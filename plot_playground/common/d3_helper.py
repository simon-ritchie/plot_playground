"""
A D3.js common helper module.

Notes
-----
Js string is using bracket, that conflict python string format.
Therefore, r character is required before quotation.
"""

from IPython.display import display, HTML

from plot_playground.common import settings


D3_REQUIRE_HTML = r"""
<script>
    requirejs.config({
        paths: {
            'd3': ['https://d3js.org/d3.{d3_version}.min'],
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
<svg id="{svg_id}" width="{svg_width}" height="{svg_height}">
</svg>
<script>
    require(['d3'], function(d3) {
        {js_script}
    });
</script>
"""


def exec_d3_js_script_on_jupyter(
        js_script, svg_id, svg_width, svg_height):
    """
    Execute the JavaScript code in a form that can access
    D3.js.

    Parameters
    ----------
    js_script : str
        Code of JavaScript to be executed.
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
    display(HTML(html))

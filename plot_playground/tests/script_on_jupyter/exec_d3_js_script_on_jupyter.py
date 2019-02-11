"""
Notes
-----
This file is used as a test script string on Jupyter, not as
a module.
"""

from plot_playground.common import d3_helper
from plot_playground.common.settings import TEST_SVG_ELEM_ID

js_script = r"""
d3.select("#{test_svg_elem_id}")
    .append("rect")
    .attr("width", 100)
    .attr("height", 100)
    .attr("fill", "#ff0000")
    """
js_script = js_script.replace(
    '{test_svg_elem_id}', TEST_SVG_ELEM_ID)
d3_helper.exec_d3_js_script_on_jupyter(
    js_script=js_script,
    css_str='',
    svg_id=TEST_SVG_ELEM_ID,
    svg_width=100,
    svg_height=100)

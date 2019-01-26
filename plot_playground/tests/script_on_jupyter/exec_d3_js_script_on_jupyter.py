"""
Notes
-----
This file is used as a test script string on Jupyter, not as
a module.
"""

from plot_playground.common import d3_helper

d3_helper.load_d3_on_jupyter()
js_script = r"""
d3.select("#test_svg")
    .append("rect")
    .attr("width", 100)
    .attr("height", 100)
    .attr("fill", "#ff0000")
    """
d3_helper.exec_d3_js_script_on_jupyter(
    js_script=js_script,
    svg_id='test_svg',
    svg_width=100,
    svg_height=100)

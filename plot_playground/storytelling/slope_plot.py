"""
A module of slope plot which made only some elements stand out.
"""

import numpy as np

from plot_playground.common import d3_helper
from plot_playground.common import data_helper

PATH_CSS_TEMPLATE = 'storytelling/slope_plot.css'
PATH_JS_TEMPLATE = 'storytelling/slope_plot.js'


def display_plot(
        df,
        label_column_name,
        left_value_column_name,
        right_value_column_name,
        standing_out_label_name_list,
        width=600,
        height=372,
        plot_border_size=1,
        basic_margin=20,
        font_family='-apple-system, BlinkMacSystemFont, "Helvetica Neue", YuGothic, "ヒラギノ角ゴ ProN W3", Hiragino Kaku Gothic ProN, Arial, "メイリオ", Meiryo, sans-serif',
        title='',
        title_color='#6bb2f8',
        title_font_size=25,
        description='',
        description_color='#999999',
        description_font_size=14,
        label_font_size=14,
        label_color='#999999',
        standing_out_label_font_weight='bold',
        standing_out_label_color='#6bb2f8',
        left_value_prefix='',
        left_value_suffix='',
        right_value_prefix='',
        right_value_suffix='',
        line_color='#cccccc',
        line_width=2.5,
        standing_out_line_color='#acd5ff',
        standing_out_line_width=4.0,
        circle_color='#cccccc',
        circle_radius=4,
        standing_out_circle_color='#acd5ff',
        standing_out_circle_radius=5,
        svg_id='',
    ):
    """
    Display slope plot on Jupyter.

    Parameters
    ----------
    df : pandas.DataFrame
        Data frame to be plotted. Label's column, left value's column,
        right's value column are required.
    label_column_name : str
        Column name of the label.
    left_value_column_name : str
        Column name of the value on the left.
    right_value_column_name : str
        Column name of the value on the right.
    standing_out_label_name_list : list of str
        List of label names to make it stand out.
    width : int, default 600
        Width of the plot.
    height : int default 372
        Height of the plot.
    plot_border_size : int, default 1
        The size of the line around the plot.
    basic_margin : int, default 20
        Basic margin value.
    font_family : str
        Font setting.
    title : str, default ''
        The title of the plot.
    title_color : str, default '#6bb2f8'
        Text color of the title.
    title_font_size : int
        The font size of the title.
    description : str, default ''
        Description text.
    description_color : str, default '#999999'
        Text color of the description.
    description_font_size : int, default 14
        Font size of the description.
    label_font_size : int, default 14
        Font size of label.
    label_color : str, default '#999999'
        Font color of label.
    standing_out_label_font_weight : str, default 'bold'
        Weight setting of the label to make it stand out.
    standing_out_label_color : str, default '#6bb2f8'
        Text color of the label to make it stand out.
    left_value_prefix : str, default ''
        A string to add before the value on the left, e.g., $.
    left_value_suffix : str, default ''
        A string to add after the value on the left, e.g., %.
    right_value_prefix : str, default ''
        A string to add before the value on the right, e.g., $.
    right_value_suffix : str, default ''
        A string to add after the value on the right, e.g., %.
    line_color : str, default '#cccccc'
        Normal line color.
    line_width : float, default 2.5
        Normal line width.
    standing_out_line_color : str, default '#acd5ff'
        The color of the line that makes it stand out.
    standing_out_line_width : float, default 4.0
        Width of the line to make it stand out.
    circle_color : str, default '#cccccc'
        The color of a normal circle.
    circle_radius : int, default 4
        The radius of a normal circle.
    standing_out_circle_color : '#acd5ff'
        The color of the circle to stand out.
    standing_out_circle_radius : int, default 5
        Radius of the circle to stand out.
    svg_id : str, default ''
        ID to set for SVG element. When an empty value is specified,
        a unique character string is generated and used.

    Returns
    -------
    plot_meta : plot_playground.common.d3_helper.PlotMeta
        An object that stores the metadata of the plot.
    """
    pass

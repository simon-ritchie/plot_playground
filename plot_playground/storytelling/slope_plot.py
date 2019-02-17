"""
A module of slope plot which made only some elements stand out.
"""

import numpy as np

from plot_playground.common import d3_helper
from plot_playground.common import data_helper
from plot_playground.common import js_helper_template_path

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
        plot_background_color='#ffffff',
        plot_border_size=1,
        plot_border_color='#cccccc',
        basic_margin=20,
        font_family='-apple-system, BlinkMacSystemFont, "Helvetica Neue", YuGothic, "ヒラギノ角ゴ ProN W3", Hiragino Kaku Gothic ProN, Arial, "メイリオ", Meiryo, sans-serif',
        title='',
        title_color='#6bb2f8',
        title_font_size=25,
        description='',
        description_color='#999999',
        description_font_size=14,
        label_font_weight='normal',
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

    See Also
    --------
    https://nbviewer.jupyter.org/github/simon-ritchie/plot_playground/blob/master/documents/storytelling_slope_plot/document.html
        Document of this plot.

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
    plot_background_color : str, default '#ffffff'
        The background color of the plot.
    plot_border_size : int, default 1
        The size of the line around the plot.
    plot_border_color : str, default '#cccccc'
        The color of the line around the plot.
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
    label_font_weight : str, default 'normal'
        Weight setting of normal label.
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
    if svg_id == '':
        svg_id = d3_helper.make_svg_id()
    css_template_str = d3_helper.read_template_str(
        template_file_path=PATH_CSS_TEMPLATE)
    css_param = {
        'svg_id': svg_id,
        'svg_border_size': plot_border_size,
        'svg_border_color': plot_border_color,
        'svg_background_color': plot_background_color,
        'font_family': font_family,
        'title_color': title_color,
        'title_font_size': title_font_size,
        'description_font_size': description_font_size,
        'description_color': description_color,
        'label_font_weight': label_font_weight,
        'label_font_size': label_font_size,
        'label_color': label_color,
        'standing_out_label_font_weight': standing_out_label_font_weight,
        'standing_out_label_color': standing_out_label_color,
        'line_color': line_color,
        'line_width': line_width,
        'standing_out_line_color': standing_out_line_color,
        'standing_out_line_width': standing_out_line_width,
        'circle_color': circle_color,
        'standing_out_circle_color': standing_out_circle_color,
    }
    css_template_str = d3_helper.apply_css_param_to_template(
        css_template_str=css_template_str,
        css_param=css_param)

    df = df.copy()
    _validate_df_columns(
        df=df, label_column_name=label_column_name,
        left_value_column_name=left_value_column_name,
        right_value_column_name=right_value_column_name,
    )
    df[label_column_name] = df[label_column_name].astype(
        np.str, copy=False)
    js_template_str = d3_helper.read_template_str(
        template_file_path=PATH_JS_TEMPLATE)
    helper_func_str_get_max_width = d3_helper.read_template_str(
        template_file_path=js_helper_template_path.GET_MAX_WIDTH)
    dataset = _make_dataset(
        df=df, label_column_name=label_column_name,
        left_value_column_name=left_value_column_name,
        right_value_column_name=right_value_column_name,
        standing_out_label_name_list=standing_out_label_name_list,
    )
    min_value = df[
        [left_value_column_name, right_value_column_name]].min().min()
    max_value = df[
        [left_value_column_name, right_value_column_name]].max().max()
    js_param = {
        'svg_id': svg_id,
        'svg_width': width,
        'svg_height': height,
        'helper_func_get_max_width': helper_func_str_get_max_width,
        'basic_margin': basic_margin,
        'font_size_label': label_font_size,
        'circle_radius': circle_radius,
        'standing_out_circle_radius': standing_out_circle_radius,
        'plot_title': title,
        'plot_description': description,
        'dataset': dataset,
        'min_value': min_value,
        'max_value': max_value,
        'left_value_prefix': left_value_prefix,
        'left_value_suffix': left_value_suffix,
        'right_value_prefix': right_value_prefix,
        'right_value_suffix': right_value_suffix,
    }
    js_template_str = d3_helper.apply_js_param_to_template(
        js_template_str=js_template_str, js_param=js_param)
    html_str = d3_helper.exec_d3_js_script_on_jupyter(
        js_script=js_template_str,
        css_str=css_template_str,
        svg_id=svg_id,
        svg_width=width,
        svg_height=height)

    plot_meta = d3_helper.PlotMeta(
        html_str=html_str,
        js_template_str=js_template_str,
        js_param=js_param,
        css_template_str=css_template_str,
        css_param=css_param)
    return plot_meta


def _make_dataset(
        df, label_column_name, left_value_column_name,
        right_value_column_name, standing_out_label_name_list):
    """
    Make the required dataset from the data frame.

    Parameters
    ----------
    df : pandas.DataFrame
        The target data frame.
    label_column_name : str
        Column name of the label.
    left_value_column_name : str
        Column name of the value on the left.
    right_value_column_name : str
        Column name of the value on the right.
    standing_out_label_name_list : list of str
        List of label names to make it stand out.

    Returns
    -------
    dataset : list of dicts
        The generated data set. The following keys are set to
        the dictionary in the list.
        - label : str
        - left : int or float
        - right : int or float
        - isStandingOutData : int, 0 or 1.
    """
    df = df.copy()
    df.rename(columns={
        label_column_name: 'label',
        left_value_column_name: 'left',
        right_value_column_name: 'right',
    }, inplace=True)
    dataset = []
    for index, sr in df.iterrows():
        is_in = sr['label'] in standing_out_label_name_list
        if is_in:
            continue
        data_dict = {
            'label': sr['label'],
            'left': sr['left'],
            'right': sr['right'],
            'isStandingOutData': 0,
        }
        dataset.append(data_dict)
    for index, sr in df.iterrows():
        is_in = sr['label'] in standing_out_label_name_list
        if not is_in:
            continue
        data_dict = {
            'label': sr['label'],
            'left': sr['left'],
            'right': sr['right'],
            'isStandingOutData': 1,
        }
        dataset.append(data_dict)
    return dataset


def _validate_df_columns(
        df, label_column_name, left_value_column_name,
        right_value_column_name):
    """
    Check the structure and value of columns in the data frame.

    Parameters
    ----------
    df : pandas.DataFrame
        The target data frame.
    label_column_name : str
        Column name of the label.
    left_value_column_name : str
        Column name of the value on the left.
    right_value_column_name : str
        Column name of the value on the right.

    Raises
    ------
    ValueError
        - If the necessary columns are not included.
        - The value is not a numerical value.
        - The value contains a missing value.
    """
    is_in = label_column_name in df.columns
    if not is_in:
        err_mgs = 'The column specified for label_column_name is not included: %s' \
            % label_column_name
        raise ValueError(err_mgs)
    is_in = left_value_column_name in df.columns
    if not is_in:
        err_mgs = 'The column specified for left_value_column_name is not included: %s' \
            % left_value_column_name
        raise ValueError(err_mgs)
    is_in = right_value_column_name in df.columns
    if not is_in:
        err_mgs = 'The column specified for right_value_column_name is not included: %s' \
            % right_value_column_name
        raise ValueError(err_mgs)

    data_helper.validate_all_values_are_numeric(
        df=df, columns=[left_value_column_name, right_value_column_name])
    data_helper.validate_null_value_not_exists_in_df(
        df=df, columns=[left_value_column_name, right_value_column_name])

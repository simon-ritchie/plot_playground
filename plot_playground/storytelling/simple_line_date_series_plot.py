"""
A module that handles a plot of a polygonal line that makes only
specific line elements stand out.
"""

import numpy as np

from plot_playground.common import d3_helper
from plot_playground.common import data_helper

PATH_CSS_TEMPLATE = 'storytelling/simple_line_date_series_plot.css'
PATH_JS_TEMPLATE = 'storytelling/simple_line_date_series_plot.js'


def display_plot(
        df,
        date_column,
        normal_columns,
        stands_out_columns,
        width=600,
        height=372,
        title='',
        title_color='#6bb2f8',
        title_font_size=25,
        description='',
        description_font_size=14,
        description_color='#999999',
        y_axis_label='',
        y_axis_prefix='',
        y_axis_suffix='',
        axis_line_color='#999999',
        axis_text_color='#999999',
        axis_font_size=14,
        legend_font_size=14,
        legend_color='#999999',
        stands_out_legend_font_size=14,
        stands_out_legend_font_color='#6bb2f8',
        stands_out_legend_font_weight='bold',
        line_color='#e8e8e8',
        line_size=2.5,
        stands_out_line_color='#acd5ff',
        stands_out_line_size=4.0,
        outer_margin=20,
        x_ticks=5,
        y_ticks=5,
        plot_background_color='#ffffff',
        plot_margin_left=0,
        outer_border_size=1,
        outer_border_color='#cccccc',
        font_family='-apple-system, BlinkMacSystemFont, "Helvetica Neue", YuGothic, "ヒラギノ角ゴ ProN W3", Hiragino Kaku Gothic ProN, Arial, "メイリオ", Meiryo, sans-serif',
        svg_id='',
    ):
    """
    Display a simple line plot on Jupyter. Only particular ones
    are markedly visible.

    See Also
    --------
    https://nbviewer.jupyter.org/github/simon-ritchie/plot_playground/blob/master/documents/storytelling_simple_line_date_series_plot/document.html
        Document of this plot.

    Parameters
    ----------
    df : pandas.DataFrame
        Data frame to be plotted. A date column is required.
    date_column : str
        Column name of the date in the data frame.
    normal_columns : list of str
        A list of the column names of targets for which inconspicuous
        colors are set.
    stands_out_columns : list of str
        A list of column names for which prominent colors are set.
    width : int, default 600
        Width of the plot.
    height : int default 372
        Height of the plot.
    title : str, default ''
        The title of the plot. If an empty character is specified,
        the title is not displayed.
    title_color : str, default '#6bb2f8'
        Title color setting.
    title_font_size : int, defaul 25
        Title font size.
    description : str, default ''
        Explanatory text. It is displayed under the title. It is not
        displayed when an empty character is specified.
    description_font_size : int, default 14
        The font size of description.
    description_color : str, default '#999999'
        The color setting of description.
    y_axis_label : str, default ''
        The label to set on the y axis. It is displayed in a rotated state.
    y_axis_prefix : str, default ''
        A string to set before the value of the y axis.
        e.g., $.
    y_axis_suffix : str, default ''
        A character string to be set after the value of the y axis.
        e.g., %.
    axis_line_color : str, default '#999999'
        Color of axis line.
    axis_text_color : str, defaul '#999999'
        The font color of the axis.
    axis_font_size : int, default 14
        The font size of the axis.
    legend_font_size : int, default 14
        The font size of the legend.
    legend_color : str, default '#999999'
        The color setting of legend.
    stands_out_legend_font_size : int, default 14
        The legend's font size of the place to stand out.
    stands_out_legend_font_color : str, default '#6bb2f8'
        The legend's font color of the place to stand out.
    stands_out_legend_font_weight : str, default 'bold'
        The legend's font weight of the place to stand out.
    line_color : str, default '#e8e8e8'
        Line color of a normal polygonal line.
    line_size : float, default 2.5
        The size of a normal polygonal line.
    stands_out_line_color : str, default '#acd5ff'
        Line color of the line to make it stand out.
    stands_out_line_size : float, default 4.0
        Size of the line to stand out.
    outer_margin : int, default 20
        Edge margin of plot area.
    x_ticks : int, default 5
        Number of steps on the x axis. This number roughly varies depending
        on the value of surplus etc.
    y_ticks : int
        Number of steps in the y axis. This number roughly varies depending
        on the value of surplus etc.
    plot_background_color : str
        The background color of the plot.
    plot_margin_left : int, default 0
        The left margin of the SVG area.
    outer_border_size : int, default 1
        Plot outside border size.
    outer_border_color : str, default '#cccccc'
        Plot outside border color.
    font_family : str
        Font setting. e.g., Meiryo, sans-serif
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
        'svg_border_size': outer_border_size,
        'svg_border_color': outer_border_color,
        'font_family': font_family,
        'title_color': title_color,
        'title_font_size': title_font_size,
        'description_font_size': description_font_size,
        'description_color': description_color,
        'legend_font_size': legend_font_size,
        'legend_color': legend_color,
        'stands_out_legend_font_size': stands_out_legend_font_size,
        'stands_out_legend_font_color': stands_out_legend_font_color,
        'stands_out_legend_font_weight': stands_out_legend_font_weight,
        'axis_stroke_color': axis_line_color,
        'axis_text_color': axis_text_color,
        'axis_font_size': axis_font_size,
        'line_color': line_color,
        'line_size': line_size,
        'stands_out_line_color': stands_out_line_color,
        'stands_out_line_size': stands_out_line_size,
    }
    css_template_str = d3_helper.apply_css_param_to_template(
        css_template_str=css_template_str,
        css_param=css_param
    )

    df = df.copy()
    _validate_df_columns(
        df=df, date_column=date_column, normal_columns=normal_columns,
        stands_out_columns=stands_out_columns)
    df = data_helper.cast_df_column_to_date_str(
        df=df, column_name=date_column)
    merged_column_list = [*normal_columns, *stands_out_columns]
    data_helper.validate_null_value_not_exists_in_df(
        df=df, columns=merged_column_list)
    data_helper.validate_all_values_are_numeric(
        df=df, columns=merged_column_list)
    dataset_df = df.loc[:, [date_column, *merged_column_list]]
    dataset = dataset_df.to_dict(orient='record')
    legend_dataset = _make_legend_dataset(
        df=df, date_column=date_column, normal_columns=normal_columns,
        stands_out_columns=stands_out_columns)
    year_str_list = _make_year_str_list(df=df, date_column=date_column)
    y_axis_min = data_helper.get_df_min_value(
        df=df, columns=merged_column_list)
    y_axis_min = min(0, y_axis_min)
    y_axis_max = data_helper.get_df_max_value(
        df=df, columns=merged_column_list)
    js_param = {
        'svg_id': svg_id,
        'svg_width': width,
        'svg_height': height,
        'svg_background_color': plot_background_color,
        'svg_margin_left': plot_margin_left,
        'outer_margin': outer_margin,
        'x_ticks': x_ticks,
        'y_ticks': y_ticks,
        'y_axis_prefix': y_axis_prefix,
        'y_axis_suffix': y_axis_suffix,
        'plot_title': title,
        'plot_description': description,
        'dataset': dataset,
        'date_column': date_column,
        'column_list': normal_columns,
        'stands_out_column_list': stands_out_columns,
        'legend_dataset': legend_dataset,
        'year_str_list': year_str_list,
        'y_axis_min': y_axis_min,
        'y_axis_max': y_axis_max,
        'y_axis_label': y_axis_label,
        'x_axis_min': df[date_column].min(),
        'x_axis_max': df[date_column].max(),
    }
    js_template_str = d3_helper.read_template_str(
        template_file_path=PATH_JS_TEMPLATE)
    js_template_str = d3_helper.apply_js_param_to_template(
        js_template_str=js_template_str,
        js_param=js_param
    )
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


def _make_year_str_list(df, date_column):
    """
    Generate a list containing year strings to be used on the x axis.

    Parameters
    ----------
    df : DataFrame
        A data frame containing a column of date string.
    date_column : str
        Column name of the date.

    Returns
    -------
    year_str_list : list of str
        A list containing characters at the beginning of the year.
        e.g., ["2018-01-01", "2019-01-01"]
    """
    min_date_str = df[date_column].min()
    date_unique_arr = df[date_column].unique()
    year_str_list = []
    for date_str in date_unique_arr:
        year_str = data_helper.get_year_str_from_date_str(
            date_str=date_str)
        year_str_list.append(year_str)
    year_str_list = np.unique(year_str_list).tolist()
    year_str_list.sort()
    for i, year_str in enumerate(year_str_list):
        year_str += '-01-01'
        if year_str < min_date_str:
            year_str = min_date_str
        year_str_list[i] = year_str
    return year_str_list


def _make_legend_dataset(
        df, date_column, normal_columns, stands_out_columns):
    """
    Make a data set for the legend.

    Parameters
    ----------
    df : pandas.DataFrame
        Data frame to be plotted. A date column is required.
    date_column : str
        Column name of the date in the data frame.
    normal_columns : list of str
        A list of the column names of targets for which inconspicuous
        colors are set.
    stands_out_columns : list of str
        A list of column names for which prominent colors are set.

    Returns
    -------
    legend_dataset : list of dicts
        A list of dictionaries containing data for the legend.
        The following keys are set in the dictionary.
        - key : str -> Column names excluding dates are set.
        - value : The value of the last date is set.
    """
    df.sort_values(by=date_column, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df_len = len(df)
    legend_dataset = []
    merged_columns = [*normal_columns, *stands_out_columns]
    for column_name in merged_columns:
        last_date_val = df.loc[df_len - 1, column_name]
        legend_dataset.append({
            'key': column_name,
            'value': last_date_val,
        })
    return legend_dataset


def _validate_df_columns(
        df, date_column, normal_columns, stands_out_columns):
    """
    Check that the specified column exists in the data frame.

    Parameters
    ----------
    df : pandas.DataFrame
        Data frame to be checked.
        df, date_column, normal_columns, stands_out_columns):
    date_column : str
        Column name of the date in the data frame.
    normal_columns : list of str
        A list of the column names of targets for which inconspicuous
        colors are set.
    stands_out_columns : list of str
        A list of column names for which prominent colors are set.

    Raises
    ------
    ValueError
        If the required column is not included in the data frame.
    """
    has_column = date_column in df.columns
    if not has_column:
        err_msg = 'The specified date column is not included in the data frame.'
        raise ValueError(err_msg)
    merged_column_list = [*normal_columns, *stands_out_columns]
    for column_name in merged_column_list:
        has_column = column_name in df.columns
        if not has_column:
            err_msg = 'The specified column is not included in the data frame : %s' \
                % column_name
            raise ValueError(err_msg)

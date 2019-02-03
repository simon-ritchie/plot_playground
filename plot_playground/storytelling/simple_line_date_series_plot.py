"""
A module that handles a plot of a polygonal line that makes only
specific line elements stand out.
"""

def display(
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
        line_color='#cccccc',
        line_size=2.5,
        stands_out_line_color='#acd5ff',
        stands_out_line_size=4.0,
        outer_margin=20,
        x_ticks=5,
        y_ticks=5,
        outer_border_size=1,
        outer_border_color='#999999',
        font_family='-apple-system, BlinkMacSystemFont, "Helvetica Neue", YuGothic, "ヒラギノ角ゴ ProN W3", Hiragino Kaku Gothic ProN, Arial, "メイリオ", Meiryo, sans-serif',
    ):
    """
    Display a simple line graph on Jupyter. Only particular ones
    are markedly visible.

    Parameters
    ----------
    df : DataFrame
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
    line_color : str, default '#cccccc'
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
    outer_border_size : int, default 1
        Plot outside border size.
    outer_border_color : str, default '#999999'
        Plot outside border color.
    font_family : str
        Font setting. e.g., Meiryo, sans-serif
    """
    pass

/*
Python Parameters
-----------------
{svg_id} : str
    SVG elemnt's ID.
{svg_width} : int
    Width of SVG area.
{svg_height} : int
    Height of SVG area.
{svg_background_color} : str
    The background color of the svg.
{svg_margin_left} : int
    The left margin of the SVG area. It is basically set by position
    adjustment on Jupyter.
{outer_margin} : int
    Edge margin of SVG area.
{x_ticks} : int
    Number of steps on the x axis. This number roughly varies depending
    on the value of surplus etc.
{y_ticks} : int
    Number of steps in the y axis. This number roughly varies depending
    on the value of surplus etc.
{y_axis_prefix} : str
    A string to set before the value of the y axis.
    e.g., $.
{y_axis_suffix} : str
    A character string to be set after the value of the y axis.
    e.g., %.
{plot_title} : str
    The title of the plot.
{plot_description} : str
    A description of the plot. It is set under the title.
{dataset} : list of dicts
    Data set to set. The following keys are required in the dictionary.
    - date : A string of dates of the form "%Y-%m-%d".
    - other key : Any other key that stores the value of int or float.
{column_list} : list of str
    A list of the column names of targets for which inconspicuous
    colors are set.
{stands_out_column_list} : list of str
    A list of column names for which prominent colors are set.
{legend_dataset} : list of dicts
    A list containing values ​​to be set in the legend. It is used to
    calculate the Y coordinate. Specify a dictionary containing the
    key names key and value. Set the column name to key and value to
    the last value of time series.
    e.g., [{"key": "A", "value": 100}]
{year_str_list} : list of str
    A list containing characters at the beginning of the year.
    e.g., ["2018-01-01", "2019-01-01"]
{y_axis_min} : int or float
    The minimum value on the y axis. Set to 0 or a negative value.
{y_axis_max} : int or float
    Maximum value of y axis.
{y_axis_label} : str
    The label to set on the y axis. It is displayed in a rotated state.
{x_axis_min} : str
    String with the oldest date on the x axis.
{x_axis_max} : str
    String of the last date on the x axis.
 */

const SVG_ID = "{svg_id}";
const SVG_WIDTH = {svg_width};
const SVG_HEIGHT = {svg_height};
const SVG_BACKGROUND_COLOR = "{svg_background_color}";
const SVG_MARGIN_LEFT = {svg_margin_left};
const OUTER_MARGIN = {outer_margin};
const X_TICKS = {x_ticks};
const Y_TICKS = {y_ticks};
const Y_AXIS_PREFIX = "{y_axis_prefix}";
const Y_AXIS_SUFFIX = "{y_axis_suffix}";
const PLOT_TITLE_TXT = "{plot_title}";
const PLOT_DESCRIPTION_TXT = "{plot_description}";

var dateParse = d3.timeParse("%Y-%m-%d");
var dataset = {dataset};
for (var i = 0; i < dataset.length; i++) {
    var dataDict = dataset[i];
    dataDict["date"] = dateParse(dataDict["date"]);
}
const COLUMN_LIST = {column_list};
const STANDS_OUT_COLUMN_LIST = {stands_out_column_list};
var MERGED_COLUMN_LIST = COLUMN_LIST.concat(STANDS_OUT_COLUMN_LIST);
const LEGEND_DATASET = {legend_dataset};
const LEGEND_KEY = function(d) {
    return d.key;
}
var yearDataset = {year_str_list};
for (var i = 0; i < yearDataset.length; i++) {
    yearDataset[i] = dateParse(yearDataset[i]);
}
const Y_AXIS_MIN = {y_axis_min};
const Y_AXIS_MAX = {y_axis_max} * 1.1;
const Y_AXIS_LABEL = "{y_axis_label}";
const X_AXIS_MIN = dateParse("{x_axis_min}");
const X_AXIS_MAX = dateParse("{x_axis_max}");

var svg = d3.select("#" + SVG_ID)
    .style("background-color", SVG_BACKGROUND_COLOR)
    .style("margin-left", SVG_MARGIN_LEFT);

var plotBaseLineY = 0;
if (PLOT_TITLE_TXT !== "") {
    var plotTitle = svg.append("text")
        .attr("x", OUTER_MARGIN)
        .attr("y", OUTER_MARGIN)
        .attr("dominant-baseline", "hanging")
        .text(PLOT_TITLE_TXT)
        .classed("title font", true);
    var plotTitleBBox = plotTitle.node().getBBox();
    plotBaseLineY += plotTitleBBox.y + plotTitleBBox.height;
}

if (PLOT_DESCRIPTION_TXT !== "") {
    var plotDescription = svg.append("text")
        .attr("x", OUTER_MARGIN)
        .attr("y", plotBaseLineY + 10)
        .attr("dominant-baseline", "hanging")
        .text(PLOT_DESCRIPTION_TXT)
        .classed("description font", true);
    var plotDesciptionBBox = plotDescription.node().getBBox();
    plotBaseLineY += plotDesciptionBBox.height + 10;
}

var legend = svg.selectAll("legend")
    .data(LEGEND_DATASET, LEGEND_KEY)
    .enter()
    .append("text")
    .text(function(d) {
        return d.key;
    })
    .attr("dominant-baseline", "central");
legend.each(function(d) {
    var className;
    if (STANDS_OUT_COLUMN_LIST.indexOf(d.key) >= 0) {
        className = "legend stands-out-legend font";
    }else {
        className = "legend font";
    }
    d3.select(this)
        .classed(className, true);
})

var yLabelMarginAdjust = 0;
if (Y_AXIS_LABEL !== "") {
    var yAxisLabel = svg.append("text")
        .text(Y_AXIS_LABEL)
        .attr("transform", "rotate(270)")
        .attr("text-anchor", "end")
        .attr("dominant-baseline", "text-before-edge")
        .classed("font y-axis-label", true);
    yAxisLabel.attr("x", -plotBaseLineY - OUTER_MARGIN + 1)
        .attr("y", OUTER_MARGIN - 3);
    var yAxisLabelBBox = yAxisLabel.node()
        .getBBox();
    yLabelMarginAdjust = yAxisLabelBBox.height + 2;
}
var yAxisScale = d3.scaleLinear()
    .domain([Y_AXIS_MIN, Y_AXIS_MAX])
    .range([SVG_HEIGHT - OUTER_MARGIN, plotBaseLineY + OUTER_MARGIN]);
var yAxis = d3.axisLeft()
    .scale(yAxisScale)
    .ticks(Y_TICKS)
    .tickFormat(function (d) {
        var tickFormat = d;
        if (Y_AXIS_PREFIX !== "") {
            tickFormat = Y_AXIS_PREFIX + tickFormat;
        }
        if (Y_AXIS_SUFFIX !== "") {
            tickFormat += Y_AXIS_SUFFIX;
        }
        return tickFormat;
    });
var yAxisGroup = svg.append("g")
    .classed("y-axis font", true)
    .call(yAxis);
var yAxisBBox = yAxisGroup
    .node()
    .getBBox();
var yAxisPositionX = OUTER_MARGIN + yAxisBBox.width + yLabelMarginAdjust;
yAxisGroup.attr("transform", "translate(" + yAxisPositionX + ", 0)");

var xAxisScale = d3.scaleTime()
    .domain([X_AXIS_MIN, X_AXIS_MAX])
    .range([yAxisPositionX, SVG_WIDTH - OUTER_MARGIN]);

var yearFormat = d3.timeFormat("%Y");
var year = svg.selectAll("year")
    .data(yearDataset)
    .enter()
    .append("text")
    .text(function(d) {
        return yearFormat(d);
    })
    .attr("text-anchor", "middle")
    .attr("x", function(d) {
        return xAxisScale(d);
    })
    .attr("y", SVG_HEIGHT - OUTER_MARGIN)
    .classed("font x-axis-year", true);
var yearBBox = year.node()
    .getBBox()

var xAxis = d3.axisBottom()
    .scale(xAxisScale)
    .ticks(X_TICKS)
    .tickFormat(d3.timeFormat("%m/%d"));
var xAxisGroup = svg.append("g")
    .classed("x-axis font", true)
    .call(xAxis)
var xAxisBBox = xAxisGroup
    .node()
    .getBBox();
xAxisPositionY = parseInt(
    SVG_HEIGHT - OUTER_MARGIN - xAxisBBox.height - yearBBox.height);
xAxisGroup.attr(
    "transform",
    "translate(0, " + xAxisPositionY + ")");

yAxisScale.range([xAxisPositionY, plotBaseLineY + OUTER_MARGIN]);
yAxis.scale(yAxisScale);
yAxisGroup.call(yAxis);

var legendMaxWidth = 0;
svg.selectAll(".legend").each(function(d) {
    var width = d3.select(this)
        .node()
        .getBBox()["width"];
    legendMaxWidth = Math.max(legendMaxWidth, width);
});
svg.selectAll(".legend")
    .attr("x", function(d) {
        return SVG_WIDTH - OUTER_MARGIN - legendMaxWidth;
    })
    .attr("y", function(d) {
        return yAxisScale(d.value);
    });
xAxisScale.range(
    [yAxisPositionX, SVG_WIDTH - OUTER_MARGIN - legendMaxWidth - 10]);
xAxis.scale(xAxisScale);
xAxisGroup.call(xAxis);
year.attr("x", function(d) {
    return xAxisScale(d);
});

var lineGroup = svg.append("g")
    .attr("id", "{svg_id}-lines");
for (var i = 0; i < MERGED_COLUMN_LIST.length; i++) {
    var columnName = MERGED_COLUMN_LIST[i];
    var line = d3.line()
        .x(function (d) {
            return xAxisScale(d.date);
        })
        .y(function (d) {
            return yAxisScale(d[columnName]);
        });
    if (STANDS_OUT_COLUMN_LIST.indexOf(columnName) >= 0) {
        className = "stands-out-line";
    }else {
        className = "line";
    }
    lineGroup.append("path")
        .datum(dataset)
        .classed(className, true)
        .attr("d", line);
}

var xAxisScaleRange = xAxisScale.range();
var yAxisScaleRange = yAxisScale.range();
svg.append("clipPath")
    .attr("id", "{svg_id}-plotAreaClipPath")
    .append("rect")
    .attr("x", xAxisScaleRange[0] + 1)
    .attr("y", yAxisScaleRange[1])
    .attr("width", xAxisScaleRange[1] - xAxisScaleRange[0])
    .attr("height", yAxisScaleRange[0] - yAxisScaleRange[1] - 1);
d3.select("#{svg_id}-lines")
    .attr("clip-path", "url(#{svg_id}-plotAreaClipPath)");

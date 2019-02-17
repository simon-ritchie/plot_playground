/**
Python Parameters
-----------------
{svg_id} : str
    SVG elemnt's ID.
{svg_width} : int
    Width of SVG area.
{svg_height} : int
    Height of SVG area.
{helper_func_get_max_width} : str
    A string of helper functions to get the maximum width of elements.
{basic_margin} : int
    Basic margin value.
{font_size_label} : int
    The font size of the label.
{circle_radius} : int
    The radius of the normal circle at the end of the slope.
{standing_out_circle_radius} : int
    Radius of the circle to stand out.
{plot_title} : str
    The title of the plot.
{plot_description} : str
    A description of the plot. It is set under the title.
{dataset} : list of dicts
    Dataset to set. The following keys are required in the dictionary.
    - label : str -> The label of the element.
    - left : int or float -> Left value of slope.
    - right : int or float -> Right value of slope.
    - isStandingOutData : int -> 0 or 1. Set 1 for data to make
        it stand out.
{min_value} : int or float
    Minimum value of the plot.
{max_value} : int or float
    Maximum value of the plot.
{left_value_prefix} : str
    String to set before the value on the left side.
{left_value_suffix} : str
    String to set after the value on the left side.
{right_value_prefix} : str
    String to set before the value on the right side.
{right_value_suffix} : str
    String to set after the value on the right side.
*/


{helper_func_get_max_width}


const SVG_ID = "{svg_id}";
const SVG_WIDTH = {svg_width};
const SVG_HEIGHT = {svg_height};
const BASIC_MARGIN = {basic_margin};
const FONT_SIZE_LABEL = {font_size_label};
const CIRCLE_RADIUS = {circle_radius};
const STANDING_OUT_CIRCLE_RADIUS = {standing_out_circle_radius};
const PLOT_TITLE_TXT = "{plot_title}";
const PLOT_DESCRIPTION_TXT = "{plot_description}";
const COLUMN_NAME_LABEL = "label";
const COLUMN_NAME_LEFT = "left";
const COLUMN_NAME_RIGHT = "right";
const DATASET = {dataset};
const MIN_VALUE = {min_value};
const MAX_VALUE = {max_value};
const LEFT_VALUE_PREFIX = "{left_value_prefix}";
const LEFT_VALUE_SUFFIX = "{left_value_suffix}";
const RIGHT_VALUE_PREFIX = "{right_value_prefix}";
const RIGHT_VALUE_SUFFIX = "{right_value_suffix}";
const FONT_POSITION_ADJUST = 2;

svg = d3.select("#{svg_id}");

var plotBaseLineY = 0;
if (PLOT_TITLE_TXT !== "") {
    var plotTitle = svg.append("text")
        .attr("x", BASIC_MARGIN - FONT_POSITION_ADJUST)
        .attr("y", BASIC_MARGIN)
        .attr("dominant-baseline", "hanging")
        .text(PLOT_TITLE_TXT)
        .classed("title font", true);
    var plotTitleBBox = plotTitle.node().getBBox();
    plotBaseLineY += plotTitleBBox.y + plotTitleBBox.height;
}

if (PLOT_DESCRIPTION_TXT !== "") {
    var plotDescription = svg.append("text")
        .attr("x", BASIC_MARGIN - FONT_POSITION_ADJUST)
        .attr("y", plotBaseLineY + BASIC_MARGIN / 2)
        .attr("dominant-baseline", "hanging")
        .text(PLOT_DESCRIPTION_TXT)
        .classed("description font", true);
    var plotDesciptionBBox = plotDescription.node().getBBox();
    plotBaseLineY += plotDesciptionBBox.height + BASIC_MARGIN / 2;
}

var yScale = d3.scaleLinear()
    .domain([MIN_VALUE, MAX_VALUE])
    .range([SVG_HEIGHT - BASIC_MARGIN - 3,
            plotBaseLineY + BASIC_MARGIN + 10]);

const LABEL_CLASS = "font label";
const STANDING_OUT_CLASS = "font label standing-out-label";

var leftLabels = svg.selectAll("leftLabel")
    .data(DATASET)
    .enter()
    .append("text")
    .text(function(d) {
        return d[COLUMN_NAME_LABEL];
    })
    .attr("x", BASIC_MARGIN - FONT_POSITION_ADJUST)
    .attr("y", function(d) {
        return yScale(d[COLUMN_NAME_LEFT]);
    })
    .attr("class", function(d) {
        if (d.isStandingOutData === 1) {
            return STANDING_OUT_CLASS;
        }
        return LABEL_CLASS;
    });
var leftLabelMaxWidth = getMaxWidth(leftLabels);

var leftValues = svg.selectAll("leftValues")
    .data(DATASET)
    .enter()
    .append("text")
    .text(function(d) {
        var text = d[COLUMN_NAME_LEFT];
        if (LEFT_VALUE_PREFIX !== "") {
            text = LEFT_VALUE_PREFIX + text;
        }
        if (LEFT_VALUE_SUFFIX !== "") {
            text += LEFT_VALUE_SUFFIX;
        }
        return text;
    })
    .attr("text-anchor", "end")
    .attr("y", function(d) {
        return yScale(d[COLUMN_NAME_LEFT]);
    })
    .attr("class", function(d) {
        if (d.isStandingOutData === 1) {
            return STANDING_OUT_CLASS;
        }
        return LABEL_CLASS;
    });
var leftValueMaxWidth = getMaxWidth(leftValues);
var leftValueX = BASIC_MARGIN * 2 + leftLabelMaxWidth + leftValueMaxWidth - FONT_POSITION_ADJUST * 2;
leftValues.attr("x", function(d) {
    return leftValueX;
});
var leftValuesBBoxList = [];
leftValues.each(function(d) {
    var leftValuesBBox = d3.select(this)
        .node()
        .getBBox();
    leftValuesBBoxList.push(leftValuesBBox);
});

var rightLabels = svg.selectAll("rightLabel")
    .data(DATASET)
    .enter()
    .append("text")
    .text(function(d) {
        return d[COLUMN_NAME_LABEL];;
    })
    .attr("text-anchor", "end")
    .attr("x", SVG_WIDTH - BASIC_MARGIN - FONT_POSITION_ADJUST)
    .attr("y", function(d) {
        return yScale(d[COLUMN_NAME_RIGHT]);
    })
    .attr("class", function(d) {
        if (d.isStandingOutData === 1) {
            return STANDING_OUT_CLASS;
        }
        return LABEL_CLASS;
    });
var rightLabelMaxWidth = getMaxWidth(rightLabels);

var rightValues = svg.selectAll("rightValues")
    .data(DATASET)
    .enter()
    .append("text")
    .text(function(d) {
        var text = d[COLUMN_NAME_RIGHT];
        if (RIGHT_VALUE_PREFIX !== "") {
            text = RIGHT_VALUE_PREFIX + text;
        }
        if (RIGHT_VALUE_SUFFIX !== "") {
            text += RIGHT_VALUE_SUFFIX;
        }
        return text;
    })
    .attr("y", function(d) {
        return yScale(d[COLUMN_NAME_RIGHT]);
    })
    .attr("class", function(d) {
        if (d.isStandingOutData === 1) {
            return STANDING_OUT_CLASS;
        }
        return LABEL_CLASS;
    });
var rightValueMaxWidth = getMaxWidth(rightValues);
var rightValueX = SVG_WIDTH - BASIC_MARGIN * 2 - rightValueMaxWidth - rightLabelMaxWidth;
rightValues.attr("x", function(d) {
    return rightValueX;
});
var rightValuesBBoxList = [];
rightValues.each(function(d) {
    var rightValuesBBox = d3.select(this)
        .node()
        .getBBox();
    rightValuesBBoxList.push(rightValuesBBox);
});

const SLOPE_LEFT_X = leftValueX + BASIC_MARGIN + STANDING_OUT_CIRCLE_RADIUS;
const SLOPE_RIGHT_X = rightValueX - BASIC_MARGIN - STANDING_OUT_CIRCLE_RADIUS;
var lineGroups = svg.append("g")
    .classed("line", true);
for (var i = 0; i < DATASET.length; i++) {
    var line = lineGroups.append("line")
        .attr("x1", SLOPE_LEFT_X)
        .attr("y1", leftValuesBBoxList[i].y + leftValuesBBoxList[i].height / 2)
        .attr("x2", SLOPE_RIGHT_X)
        .attr("y2", rightValuesBBoxList[i].y + rightValuesBBoxList[i].height / 2);
    var dataDict = DATASET[i];
    if (dataDict["isStandingOutData"] === 1) {
        line.classed("standing-out-line", true);
    }
}
var circleGroup = svg.append("g")
    .classed("circle", true);
for (var i = 0; i < DATASET.length; i++) {
    var dataDict = DATASET[i];
    var leftCircle = circleGroup.append("circle")
        .attr("r", CIRCLE_RADIUS)
        .attr("cx", SLOPE_LEFT_X)
        .attr("cy", leftValuesBBoxList[i].y + leftValuesBBoxList[i].height / 2);

    var rightCircle = circleGroup.append("circle")
        .attr("cx", SLOPE_RIGHT_X)
        .attr("cy", rightValuesBBoxList[i].y + rightValuesBBoxList[i].height / 2);

    if (dataDict["isStandingOutData"] === 1) {
        leftCircle.attr("r", STANDING_OUT_CIRCLE_RADIUS)
            .classed("standing-out-circle", true);
        rightCircle.attr("r", STANDING_OUT_CIRCLE_RADIUS)
            .classed("standing-out-circle", true);
    }else {
        leftCircle.attr("r", CIRCLE_RADIUS);
        rightCircle.attr("r", CIRCLE_RADIUS);
    }
}

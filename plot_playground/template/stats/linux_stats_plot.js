/**
Python Parameters
-----------------
{svg_id} : str
    SVG elemnt's ID.
{gpu_num} : int
    Number of GPUs.
{csv_log_file_path} : str
    CSV log file path.
{js_helper_func_get_b_box_width} : str
    A string of helper function to get the bounding box width of the
    target element.
 */

const SVG_ID = "{svg_id}";
const BASIC_MARGIN = 20;
const PLOT_UNIT_WIDTH = 700;
const PLOT_UNIT_HEIGHT = 200;
const PLOT_X = 1 + BASIC_MARGIN;
const GPU_NUM = {gpu_num};
const LOG_FILE_PATH = "{csv_log_file_path}";
const COLUMN_NAME_MEMORY_USAGE = "memory usage (MB)";
const COLUMN_NAME_DISK_USAGE = "disk usage (GB)";
const INTERVAL_SECONDS = 2;
const AXIS_TICKS = 5;
const ANIMATION_DURATION = 200;

{js_helper_func_get_b_box_width}

/**
 * Gets the column name of memory usage of the GPU.
 *
 * @param {int} gpuIndex: Index of target GPU (Starting
 * from zero).
 *
 * @return {String} GPU column name.
 */
function getGPUColumnName(gpuIndex) {
    return "gpu(" + gpuIndex + ") memory usage (MB)";
}

var windowFocused = true;
window.onfocus = function() {
    windowFocused = true;
}
window.onblur = function() {
    windowFocused = false;
}

var svg = d3.select("#{svg_id}");

const MEMORY_USAGE_PLOT_Y = 1 + BASIC_MARGIN;
var memoryUsagePlotBorderRect = svg.append("rect")
    .attr("width", PLOT_UNIT_WIDTH - 2 - BASIC_MARGIN * 2)
    .attr("height", PLOT_UNIT_HEIGHT - 2)
    .classed("outer-border-rect", true)
    .attr("x", PLOT_X)
    .attr("y", 1 + BASIC_MARGIN);

const DISK_USAGE_PLOT_Y = PLOT_UNIT_HEIGHT + BASIC_MARGIN * 2 + 1;
var diskUsagePlotBorderRect = svg.append("rect")
    .attr("width", PLOT_UNIT_WIDTH - 2 - BASIC_MARGIN * 2)
    .attr("height", PLOT_UNIT_HEIGHT - 2)
    .classed("outer-border-rect", true)
    .attr("x", PLOT_X)
    .attr("y", DISK_USAGE_PLOT_Y);

var gpuMemoryUsagePlotYList = [];
var gpuMemoryUsagePlotBorderRectList = [];
for (var i = 0; i < GPU_NUM; i++) {
    var gpuMemoryUsagePlotY = PLOT_UNIT_HEIGHT * (2 + i) + BASIC_MARGIN * (3 + i) + 1;
    gpuMemoryUsagePlotYList.push(gpuMemoryUsagePlotY);
    var gpuMemoryUsagePlotBorderRect = svg.append("rect")
        .attr("width", PLOT_UNIT_WIDTH - 2 - BASIC_MARGIN * 2)
        .attr("height", PLOT_UNIT_HEIGHT - 2)
        .classed("outer-border-rect", true)
        .attr("x", PLOT_X)
        .attr("y", gpuMemoryUsagePlotY);
    gpuMemoryUsagePlotBorderRectList.push(
        gpuMemoryUsagePlotBorderRect
    );
}

var rowConverter = function(d) {
    var rowDict = {
        memoryUsage: parseInt(d[COLUMN_NAME_MEMORY_USAGE]),
        diskUsage: parseFloat(d[COLUMN_NAME_DISK_USAGE])
    };
    for (var i = 0; i < GPU_NUM; i++) {
        var gpuColumnName = getGPUColumnName(gpuIndex=i);
        rowDict["gpuMemoryUsage" + i] = parseInt(
            d[gpuColumnName]);
    }
    return rowDict;
}

var memoryUsageYScale = d3.scaleLinear()
    .range([
        MEMORY_USAGE_PLOT_Y + PLOT_UNIT_HEIGHT - 1 - BASIC_MARGIN,
        MEMORY_USAGE_PLOT_Y + 1 + BASIC_MARGIN]);
var memoryUsageAxis = d3.axisLeft()
    .ticks(AXIS_TICKS);
var memoryUsageAxisGroup = svg.append("g")
    .classed("axis font", true);

var diskUsageYScale = d3.scaleLinear()
    .range([
        DISK_USAGE_PLOT_Y + PLOT_UNIT_HEIGHT - 1 - BASIC_MARGIN,
        DISK_USAGE_PLOT_Y + 1 + BASIC_MARGIN]);
var diskUsageAxis = d3.axisLeft()
    .ticks(AXIS_TICKS);
var diskUsageAxisGroup = svg.append("g")
    .classed("axis font", true);

var gpuMemoryUsageYScaleList = [];
var gpuMemoryUsageAxisList = [];
var gpuMemoryUsageAxisGroupList = [];
for (var i = 0; i < GPU_NUM; i++) {
    gpuMemoryUsageYScaleList.push(
        d3.scaleLinear()
            .range([
                gpuMemoryUsagePlotYList[i] + PLOT_UNIT_HEIGHT - 1 - BASIC_MARGIN,
                gpuMemoryUsagePlotYList[i] + 1 + BASIC_MARGIN
            ])
    );
    gpuMemoryUsageAxisList.push(
        d3.axisLeft()
            .ticks(AXIS_TICKS)
    );
    gpuMemoryUsageAxisGroupList.push(
        svg.append("g")
            .classed("axis font", true)
    );
}

var xScale = d3.scaleLinear();

var memoryUsageLine = d3.line()
    .x(function(d, i) {
        return xScale(i);
    })
    .y(function(d, i) {
        return memoryUsageYScale(d.memoryUsage);
    });
var memoryUsageLinePath = svg.append("path")
    .classed("value-line", true);

var diskUsageLine = d3.line()
    .x(function(d, i) {
        return xScale(i);
    })
    .y(function(d, i) {
        return diskUsageYScale(d.diskUsage);
    });
var diskUsageLinePath = svg.append("path")
    .classed("value-line", true);

var gpuMemoryUsageLinePathList = [];
for (var i = 0; i < GPU_NUM; i++) {
    var gpuMemoryUsageLinePath = svg.append("path")
        .classed("value-line", true);
    gpuMemoryUsageLinePathList.push(gpuMemoryUsageLinePath);
}

var memoryUsagePlotBorderRectBBox = memoryUsagePlotBorderRect
    .node()
    .getBBox();
const INFO_TEXT_X = memoryUsagePlotBorderRectBBox.x + memoryUsagePlotBorderRectBBox.width + BASIC_MARGIN;
const INFO_TEXT_LINE_HEIGHT = 21;
const INFO_TEXT_CLASS = "info font";
const INFO_TEXT_DOMINANT_BASELINE = "hanging";
var memoryUsageTitle = svg.append("text")
    .attr("x", INFO_TEXT_X)
    .attr("y", memoryUsagePlotBorderRectBBox.y)
    .text(COLUMN_NAME_MEMORY_USAGE.toUpperCase())
    .attr("dominant-baseline", "hanging")
    .classed(INFO_TEXT_CLASS, true);
var memoryUsageMinText = svg.append("text")
    .attr("x", INFO_TEXT_X)
    .attr("y", memoryUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT)
    .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
    .classed(INFO_TEXT_CLASS, true)
    .text("Min: 0MB");
var memoryUsageMaxText = svg.append("text")
    .attr("x", INFO_TEXT_X)
    .attr("y", memoryUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT * 2)
    .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
    .classed(INFO_TEXT_CLASS, true)
    .text("Max: 0MB");
var memoryUsageLastText = svg.append("text")
    .attr("x", INFO_TEXT_X)
    .attr("y", memoryUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT * 3)
    .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
    .classed(INFO_TEXT_CLASS, true)
    .text("Last: 0MB");

var diskUsagePlotBorderRectBBox = diskUsagePlotBorderRect
    .node()
    .getBBox();
var diskUsageTitle = svg.append("text")
    .attr("x", INFO_TEXT_X)
    .attr("y", diskUsagePlotBorderRectBBox.y)
    .text(COLUMN_NAME_DISK_USAGE.toUpperCase())
    .attr("dominant-baseline", "hanging")
    .classed(INFO_TEXT_CLASS, true);
var diskUsageMinText = svg.append("text")
    .attr("x", INFO_TEXT_X)
    .attr("y", diskUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT)
    .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
    .classed(INFO_TEXT_CLASS, true)
    .text("Min: 0GB");
var diskUsageMaxText = svg.append("text")
    .attr("x", INFO_TEXT_X)
    .attr("y", diskUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT * 2)
    .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
    .classed(INFO_TEXT_CLASS, true)
    .text("Max: 0GB");
var diskUsageLastText = svg.append("text")
    .attr("x", INFO_TEXT_X)
    .attr("y", diskUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT * 3)
    .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
    .classed(INFO_TEXT_CLASS, true)
    .text("Last: 0GB");

var gpuMemoryUsageTitleList = [];
var gpuMemoryUsageMinTextList = [];
var gpuMemoryUsageMaxTextList = [];
var gpuMemoryUsageLastTextList = [];
for (var i = 0; i < GPU_NUM; i++) {

    var gpuMemoryUsagePlotBorderRectBBox = gpuMemoryUsagePlotBorderRectList[i]
        .node()
        .getBBox();
    var gpuColumnName = getGPUColumnName(i).toUpperCase();
    gpuMemoryUsageTitleList.push(
        svg.append("text")
            .attr("x", INFO_TEXT_X)
            .attr("y", gpuMemoryUsagePlotBorderRectBBox.y)
            .text(gpuColumnName)
            .attr("dominant-baseline", "hanging")
            .classed(INFO_TEXT_CLASS, true)
    );
    var gpuMemoryUsageMinText = svg.append("text")
        .attr("x", INFO_TEXT_X)
        .attr("y", gpuMemoryUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT)
        .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
        .classed(INFO_TEXT_CLASS, true)
        .text("Min: 0MB");
    gpuMemoryUsageMinTextList.push(gpuMemoryUsageMinText);

    var gpuMemoryUsageMaxText = svg.append("text")
        .attr("x", INFO_TEXT_X)
        .attr("y", gpuMemoryUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT * 2)
        .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
        .classed(INFO_TEXT_CLASS, true)
        .text("Max: 0MB");
    gpuMemoryUsageMaxTextList.push(gpuMemoryUsageMaxText);

    var gpuMemoryUsageLastText = svg.append("text")
        .attr("x", INFO_TEXT_X)
        .attr("y", gpuMemoryUsagePlotBorderRectBBox.y + INFO_TEXT_LINE_HEIGHT * 3)
        .attr("dominant-baseline", INFO_TEXT_DOMINANT_BASELINE)
        .classed(INFO_TEXT_CLASS, true)
        .text("Last: 0MB");
    gpuMemoryUsageLastTextList.push(gpuMemoryUsageLastText);
}

const CLIP_PATH_MARGIN_WIDTH = 2000;
svg.append("clipPath")
    .attr("id", "{svg_id}-memory-usage-clip-path")
    .append("rect")
    .attr("x", -CLIP_PATH_MARGIN_WIDTH / 2)
    .attr("y", memoryUsagePlotBorderRectBBox.y + 1)
    .attr("width", memoryUsagePlotBorderRectBBox.width + CLIP_PATH_MARGIN_WIDTH)
    .attr("height", memoryUsagePlotBorderRectBBox.height - 2);
memoryUsageAxisGroup
    .style("clip-path", "url(#{svg_id}-memory-usage-clip-path)");

svg.append("clipPath")
    .attr("id", "{svg_id}-disk-usage-clip-path")
    .append("rect")
    .attr("x", -CLIP_PATH_MARGIN_WIDTH / 2)
    .attr("y", diskUsagePlotBorderRectBBox.y + 1)
    .attr("width", diskUsagePlotBorderRectBBox.width + CLIP_PATH_MARGIN_WIDTH)
    .attr("height", memoryUsagePlotBorderRectBBox.height - 2);
diskUsageAxisGroup
    .style("clip-path", "url(#{svg_id}-disk-usage-clip-path)");

for (var i = 0; i < GPU_NUM; i++) {
    gpuMemoryUsagePlotBorderRectBBox = gpuMemoryUsagePlotBorderRectList[i]
        .node()
        .getBBox();
    svg.append("clipPath")
        .attr("id", "{svg_id}-gpu-memory-usage-clip-path-" + i)
        .append("rect")
        .attr("x", -CLIP_PATH_MARGIN_WIDTH / 2)
        .attr("y", gpuMemoryUsagePlotBorderRectBBox.y + 1)
        .attr("width", gpuMemoryUsagePlotBorderRectBBox.width + CLIP_PATH_MARGIN_WIDTH)
        .attr("height", gpuMemoryUsagePlotBorderRectBBox.height - 2);
    gpuMemoryUsageAxisGroupList[i].style(
        "clip-path", "url(#{svg_id}-gpu-memory-usage-clip-path-" + i + ")");
}

var isInitialUpdate = true;

/**
 * Read the CSV and update the value of the plot.
 */
function update_plot_value() {
    if (!windowFocused) {
        return;
    }

    d3.csv(LOG_FILE_PATH, rowConverter, function(error, dataset) {
        if (error) {
            console.log(error);
            setTimeout(update_plot_value, 100);
            return;
        }
        if (!dataset || dataset.length === 0) {
            setTimeout(update_plot_value, 100);
            return;
        }
        if ($("#{svg_id}").length === 0) {
            if (timer) {
                clearInterval(timer);
                timer = null;
                return
            }
        }
        var memoryUsageMax = d3.max(dataset, function(d) {
            return d.memoryUsage;
        });
        memoryUsageYScale.domain([0, memoryUsageMax]);
        memoryUsageAxis.scale(memoryUsageYScale);
        if (isInitialUpdate) {
            memoryUsageAxisGroup.call(memoryUsageAxis);
        }else {
            memoryUsageAxisGroup
                .transition()
                .duration(ANIMATION_DURATION)
                .call(memoryUsageAxis);
        }
        var bBoxWidth = getBBoxWidth(memoryUsageAxisGroup);
        var memoryUsageAxisTransform = "translate(" + (bBoxWidth + BASIC_MARGIN * 2 + 1) + ", 0)";
        if (isInitialUpdate) {
            memoryUsageAxisGroup
                .attr("transform", memoryUsageAxisTransform);
        }else {
            setTimeout(function() {
                bBoxWidth = getBBoxWidth(memoryUsageAxisGroup);
                var memoryUsageAxisTransform = "translate(" + (bBoxWidth + BASIC_MARGIN * 2 + 1) + ", 0)";
                memoryUsageAxisGroup
                    .transition()
                    .duration(ANIMATION_DURATION)
                    .attr("transform", memoryUsageAxisTransform);
            }, ANIMATION_DURATION + 10);
        }

        var diskUsageMax = d3.max(dataset, function(d) {
            return d.diskUsage;
        });
        diskUsageYScale.domain([0, diskUsageMax]);
        diskUsageAxis.scale(diskUsageYScale);
        if (isInitialUpdate) {
            diskUsageAxisGroup.call(diskUsageAxis);
        }else {
            diskUsageAxisGroup
                .transition()
                .duration(ANIMATION_DURATION)
                .call(diskUsageAxis);
        }
        bBoxWidth = getBBoxWidth(diskUsageAxisGroup);
        var diskUsageAxisTransform = "translate(" + (bBoxWidth + BASIC_MARGIN * 2 + 1) + ", 0)";
        if (isInitialUpdate) {
            diskUsageAxisGroup
                .attr("transform", diskUsageAxisTransform);
        }else {
            setTimeout(function() {
                bBoxWidth = getBBoxWidth(diskUsageAxisGroup);
                var diskUsageAxisTransform = "translate(" + (bBoxWidth + BASIC_MARGIN * 2 + 1) + ", 0)";
                diskUsageAxisGroup
                    .transition()
                    .duration(ANIMATION_DURATION)
                    .attr("transform", diskUsageAxisTransform);
            }, ANIMATION_DURATION + 10);
        }

        for (var i = 0; i < GPU_NUM; i++) {
            var gpuMemoryUsageMax = d3.max(dataset, function(d) {
                return d["gpuMemoryUsage" + i];
            });
            gpuMemoryUsageYScaleList[i].domain(
                [0, gpuMemoryUsageMax]);
            gpuMemoryUsageAxisList[i].scale(
                gpuMemoryUsageYScaleList[i])
            if (isInitialUpdate) {
                gpuMemoryUsageAxisGroupList[i].call(
                    gpuMemoryUsageAxisList[i]);
            }else {
                gpuMemoryUsageAxisGroupList[i]
                    .transition()
                    .duration(ANIMATION_DURATION)
                    .call(gpuMemoryUsageAxisList[i]);
            }
            if (isInitialUpdate) {
                bBoxWidth = getBBoxWidth(gpuMemoryUsageAxisGroupList[i]);
                gpuMemoryUsageAxisGroupList[i]
                    .attr("transform", "translate(" + (bBoxWidth + BASIC_MARGIN * 2 + 1) + ", 0)");
            }else {
                setTimeout(function() {
                    for (var i = 0; i < GPU_NUM; i++) {
                        bBoxWidth = getBBoxWidth(gpuMemoryUsageAxisGroupList[i]);
                        gpuMemoryUsageAxisGroupList[i]
                            .transition()
                            .duration(ANIMATION_DURATION)
                            .attr("transform", "translate(" + (bBoxWidth + BASIC_MARGIN * 2 + 1) + ", 0)");
                    }
                }, ANIMATION_DURATION + 10);
            }
        }

        setTimeout(function() {
            if (!dataset || dataset.length === 0) {
                return;
            }
            var axisBBoxWidthList = [
                getBBoxWidth(memoryUsageAxisGroup),
                getBBoxWidth(diskUsageAxisGroup)
            ];
            for (var i = 0; i < GPU_NUM; i++) {
                axisBBoxWidthList.push(
                    getBBoxWidth(gpuMemoryUsageAxisGroupList[i])
                );
            }

            var datasetLen = dataset.length;
            xScale.domain([0, datasetLen - 1])
                .range([
                    d3.max(axisBBoxWidthList) + PLOT_X + BASIC_MARGIN * 2,
                    PLOT_UNIT_WIDTH - 1 - BASIC_MARGIN * 2]);

            memoryUsageLinePath
                .datum(dataset)
                .transition()
                .attr("d", memoryUsageLine);
            diskUsageLinePath
                .datum(dataset)
                .transition()
                .attr("d", diskUsageLine);
            for (var i = 0; i < GPU_NUM; i++) {
                var gpuMemoryUsageLine = d3.line()
                    .x(function(d, i) {
                        return xScale(i);
                    })
                    .y(function(d) {
                        var gpuValue = d["gpuMemoryUsage" + i];
                        return gpuMemoryUsageYScaleList[i](gpuValue);
                    });
                gpuMemoryUsageLinePathList[i]
                    .datum(dataset)
                    .transition()
                    .attr("d", gpuMemoryUsageLine);
            }

            var memoryUsageMin = parseInt(d3.min(dataset, function(d) {
                return d.memoryUsage;
            }));
            memoryUsageMinText.text("Min: " + memoryUsageMin + "MB");
            memoryUsageMaxText.text("Max: " + parseInt(memoryUsageMax) + "MB");
            var memoryUsageLast = parseInt(
                dataset[dataset.length - 1].memoryUsage);
            memoryUsageLastText.text("Last: " + memoryUsageLast + "MB");

            var diskUsageMin = parseFloat(d3.min(dataset, function(d) {
                return d.diskUsage;
            })).toFixed(2);
            diskUsageMinText.text("Min: " + diskUsageMin + "GB");
            diskUsageMaxText.text(
                "Max: " + parseFloat(diskUsageMax).toFixed(2) + "GB");
            var diskUsageLast = parseFloat(
                dataset[dataset.length - 1].diskUsage).toFixed(2);
            diskUsageLastText.text("Last: " + diskUsageLast + "GB");

            for (var i = 0; i < GPU_NUM; i++) {
                var gpuMemoryUsageMin = parseInt(d3.min(dataset, function(d) {
                    return d["gpuMemoryUsage" + i];
                }));
                gpuMemoryUsageMinTextList[i].text(
                    "Min: " + gpuMemoryUsageMin + "MB");
                gpuMemoryUsageMax = parseInt(d3.max(dataset, function(d) {
                    return d["gpuMemoryUsage" + i];
                }));
                gpuMemoryUsageMaxTextList[i].text(
                    "Max: " + gpuMemoryUsageMax + "MB");
                var gpuMemoryUsageLast = parseInt(
                    dataset[dataset.length - 1]["gpuMemoryUsage" + i]);
                gpuMemoryUsageLastTextList[i].text(
                    "Last: " + gpuMemoryUsageLast + "MB");
            }

        }, ANIMATION_DURATION + 10);

        isInitialUpdate = false;
    });
}

update_plot_value();
var timer = setInterval(
    update_plot_value,
    INTERVAL_SECONDS * 1000);

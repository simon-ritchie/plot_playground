/**
 * Get the bounding box width of the target d3 element.
 *
 * @param {Object} elem: The target d3 element.
 *
 * @return {int} The bounding box width.
 */
function getBBoxWidth(elem) {
    var bBox = elem.node()
        .getBBox();
    return parseInt(bBox.width);
}

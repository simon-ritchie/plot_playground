/**
 * Get the maximum width of the target D3 element
 * (multiple specifications possible).
 *
 * @param {Object} elems: Target elements.
 *
 * @return {int} Max Width.
 */
function getMaxWidth(elems) {
    var maxWidth = 0;
    elems.each(function(d) {
        var bBox = d3.select(this)
            .node()
            .getBBox();
        if (bBox.width > maxWidth) {
            maxWidth = bBox.width;
        }
    });
    return maxWidth;
}

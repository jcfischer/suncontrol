/* Simple color helper functions */

var ColorUtils = {};

ColorUtils.remap = function (x, oldmin, oldmax, newmin, newmax) {
    // Remap the float x from the range oldmin-oldmax to the range newmin-newmax

    // Does not clamp values that exceed min or max.
    //    For example, to make a sine wave that goes between 0 and 256:
    // remap(math.sin(time.time()), -1, 1, 0, 256)


    let zero_to_one = (x - oldmin) / (oldmax - oldmin);
    return zero_to_one * (newmax - newmin) + newmin
};

ColorUtils.clamp = function (x, minn, maxx) {
    // Restrict the float x to the range minn-maxx
    return Math.max(minn, Math.min(maxx, x));
};

ColorUtils.hsv = function (h, s, v) {
    /*
     * Converts an HSV color value to RGB.
     *
     * Normal hsv range is in [0, 1], RGB range is [0, 255].
     * Colors may extend outside these bounds. Hue values will wrap.
     *
     * Based on tinycolor:
     * https://github.com/bgrins/TinyColor/blob/master/tinycolor.js
     * 2013-08-10, Brian Grinstead, MIT License
     */

    h = (h % 1) * 6;
    if (h < 0) h += 6;

    var i = h | 0,
        f = h - i,
        p = v * (1 - s),
        q = v * (1 - f * s),
        t = v * (1 - (1 - f) * s),
        r = [v, q, p, p, t, v][i],
        g = [t, v, v, q, p, p][i],
        b = [p, p, t, v, v, q][i];

    return [r * 255, g * 255, b * 255];
};

module.exports = ColorUtils;
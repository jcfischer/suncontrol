/* Simple math helper functions */

const MathUtils = {};

MathUtils.distance = function(p1, p2) {
    let x1 = p1[0];
    let y1 = p1[1];
    let z1 = p1[2];
    let x2 = p2[0];
    let y2 = p2[1];
    let z2 = p2[2];

    return Math.sqrt((x2-x1) ** 2 +(y2-y1) ** 2 +(z2-z1) ** 2);
};

MathUtils.scale = function(factor, vec3) {
    return [factor * vec3[0], factor * vec3[1], factor * vec3[2]];
};

MathUtils.add = function(vec3a, vec3b) {
    return [vec3a[0] + vec3b[0], vec3a[1] + vec3b[1], vec3a[2] + vec3b[2]]
};

module.exports = MathUtils;
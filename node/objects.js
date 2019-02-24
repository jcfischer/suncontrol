
const math = new require('mathjs');
const ColorUtils = new require('./color_utils');

var CObject = function() {
    this.pos = [0,0,0];
    this.vec = [0,0,0];
    this.hsv = [0,0,0];
    this.color = [1,1,0];
    this.size = 0.1;
    this.max_size = 0.2;
    this.ttl = 10000;
    this.alive = true;

};

CObject.prototype.init_random = function(boundary) {
    this.random_pos(boundary);
    this.random_vec();
    this.random_color();
    this.random_ttl();
};


CObject.prototype.random_pos = function(boundary) {
    let min_bound = boundary[0],
        max_bound = boundary[1];
    let x = math.random(min_bound[0], max_bound[0]);
    let y = math.random(min_bound[1], max_bound[1]);
    let z = math.random(min_bound[2], max_bound[2]);
    this.pos = [x, y, z];
};

CObject.prototype.random_vec = function() {
    let dx = math.random(-0.4, 0.4);
    let dy = math.random(-0.4, 0.4);
    let dz = math.random(-0.4, 0.4);
    this.vec = [dx, dy, dz];
};

CObject.prototype.random_color = function() {
    this.hsv[0] = math.random();
    this.hsv[1] = math.random();
    this.hsv[2] = math.random();

};

CObject.prototype.random_ttl = function() {
    this.ttl = math.random(4000, 10000);
};

CObject.prototype.move = function(dt) {
    if (this.alive) {
        this.ttl -= dt;
        let factor = dt / 1000.0;
        this.size += factor;
        this.pos = math.add(this.pos, math.multiply(factor, this.vec));
        if (this.ttl < 1000) {
            this.hsv[2] -= factor;
        }
    }
    this.alive = this.ttl > 0;
};

CObject.prototype.draw = function(coord) {
    // returns an rgb tuple to add to the current coordinates color

    let distance = math.distance(coord, this.pos);
    //console.log(distance);

    let color = [0, 0, 0];

    if (distance < this.size + 0.1) {
        let dot = (1 / (distance + 0.0001)); //   + (time.time()*twinkle_speed % 1)
        // dot = abs(dot * 2 - 1)
        dot = ColorUtils.remap(dot, 0, 10, 0.1, 1.1);
        dot = ColorUtils.clamp(dot, -0.5, 1.1);
        // dot **=2
        dot = ColorUtils.clamp(dot, 0.0, 1);
        //console.log(dot);
        color = ColorUtils.hsv(this.hsv[0], this.hsv[1], this.hsv[2] * dot);
        //console.log(color);

    }
    //console.log(new_color);
    return color;
};

module.exports = CObject;
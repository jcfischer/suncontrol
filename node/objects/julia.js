const CObject = new require('./objects');

const ColorUtils = new require('../lib/color_utils');
const MathUtils = new require('../lib/math_utils');

// based on code from http://slicker.me/fractals/animate.htm and
// https://lodev.org/cgtutor/juliamandelbrot.html

class JuliaSet extends CObject {

    constructor(opts) {

        super();

        this.creal = -.8;
        this.cimag = .156;
        this.frame = 0;
        this.zoom_x = 1;
        this.zoom_y = 1;
        this.x = 0;
        this.y = 0;
        this.max_iterations = 256;
        this.name = "JuliaSet";
        this.zoom = opts['zoom'] || true;
        this.animate = opts['animate'] || false;
        console.log(this);
    }

    random_pos(boundary) {
        let min_bound = boundary[0],
            max_bound = boundary[1];
        this.min_boundary = min_bound;
        this.max_boundary = max_bound;

        // select a number of paramters for the animation function
        this.x = ColorUtils.remap(Math.random(), 0, 1, 0.3, 0.7);
        this.y = ColorUtils.remap(Math.random(), 0, 1, 0.3, 0.7);
        this.freq = ColorUtils.remap(Math.random(), 0, 1, 50, 150);
        console.log(this.x, this.y);

    }

    random_ttl() {
        this.ttl = ColorUtils.remap(Math.random(), 0, 1, 60000, 120000);
        console.log(this.ttl)
    }



    move(dt) {
        if (this.alive) {
            this.ttl -= dt;
        }
        this.hsv[0] += 0.0015;  // move trough the color space
        this.frame += 1;        // increase the number of the frame

        if (this.animate) {
            this.creal = -.8 + this.x * Math.sin(this.frame / (3.14 * this.freq));    // calculate the new coordinates
            this.cimag = .156 + this.y * Math.cos(this.frame / (6.28 * this.freq));   // of the c point
        } else {
            this.creal = -.8;
            this.cimag = .156;
        }
        if (this.zoom) {
            this.zoom_x += 0.02;
            this.zoom_y += 0.02;
        }
        // slowly zoom into the Set


        this.alive = this.ttl > 0;
    }

    draw(coord) {
        // returns an rgb tuple to add to the current coordinates color
        const x = coord[0];
        const y = coord[2];

        let cx = ColorUtils.remap(x, this.min_boundary[0], this.max_boundary[0], -2 / this.zoom_x, 2 / this.zoom_x);
        let cy = ColorUtils.remap(y, this.min_boundary[2], this.max_boundary[2], -1 / this.zoom_y, 1 / this.zoom_y);
        let i = 0;

        do {
            let xt = cx * cx - cy * cy + this.creal;
            cy = 2 * cx * cy + this.cimag;
            cx = xt;
            i++;
        }
        while (i < this.max_iterations && (cx * cx + cy * cy < 4));

        // hue is based on the iteration depth and the general color region we are in
        // currently.
        let hue = (i % this.max_iterations) / this.max_iterations / 3.5 + this.hsv[0];
        // value is 0 of we have more than the number of max_iterations
        // or a gradual darker color based on the iteration depth
        let v;
        if (i >= this.max_iterations) {
            v = 0;
        } else {
            v = 2*i / this.max_iterations + 0.3;
        }
        let color = ColorUtils.hsv(hue, 1, v);
        return color;
    }
}

module.exports = JuliaSet;
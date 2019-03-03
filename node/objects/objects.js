
const math = new require('mathjs');
const ColorUtils = new require('../lib/color_utils');
const MathUtils = new require('../lib/math_utils');

class CObject {

    constructor() {
        this.pos = [0,0,0];
        this.vec = [0,0,0];
        this.hsv = [0,0,0];
        this.color = [1,1,0];
        this.size = 0.1;
        this.max_size = 0.2;
        this.ttl = 10000;
        this.alive = true;
        this.name = "Generic";
    }

    init_random(opts) {
        this.random_pos(opts.boundary);
        this.random_vec();
        this.random_color(opts.primary);
        this.random_ttl();
    }

    random_pos(boundary) {
        let min_bound = boundary[0],
            max_bound = boundary[1];
        let x = math.random(min_bound[0], max_bound[0]);
        let y = math.random(min_bound[1], max_bound[1]);
        let z = math.random(min_bound[2], max_bound[2]);
        this.pos = [x, y, z];
    }

    random_vec() {
        let dx = math.random(-0.4, 0.4);
        let dy = math.random(-0.4, 0.4);
        let dz = math.random(-0.4, 0.4);
        this.vec = [dx, dy, dz];
    }

    random_color(primary = 0) {
        let spread = math.random(-0.15, 0.15);

        this.hsv[0] = primary + spread;
        // console.log(this.hsv[0]);
        this.hsv[1] = math.random();
        this.hsv[2] = math.random();
    }

    random_ttl() {
        this.ttl = math.random(2000, 5000);
    }

    move(dt) {
        if (this.alive) {
            this.ttl -= dt;
            let factor = dt / 1000.0;
            this.pos = MathUtils.add(this.pos, MathUtils.scale(factor, this.vec));

            if (this.ttl < 1000) {
                this.hsv[2] -= factor;
            }
        }
        this.alive = this.ttl > 0;
    }

    draw(coord) {
        // returns an rgb tuple to add to the current coordinates color

        let distance = MathUtils.distance(coord, this.pos);

        let color = [0, 0, 0];

        if (distance < this.size + 0.05) {
            color = ColorUtils.hsv(this.hsv[0], this.hsv[1], this.hsv[2]);
        }

        return color;
    }
}



module.exports = CObject;
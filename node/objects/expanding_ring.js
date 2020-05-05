
const CObject = new require('./objects');

const ColorUtils = new require('../lib/color_utils');
const MathUtils = new require('../lib/math_utils');

class ExpandingRing extends CObject {

    constructor() {

        super();

        this.name = "ExpandingRing";
    }

    move(dt) {
        if (this.alive) {
            this.ttl -= dt;
            let factor = dt / 1000.0;
            this.size += factor;
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
        //console.log(distance);

        let color = [0, 0, 0];

        if ((distance < this.size + 0.1) && (distance > this.size - 0.1)) {
            let dot = (1 / (distance + 0.0001)); //   + (time.time()*twinkle_speed % 1)
            // dot = abs(dot * 2 - 1)
            dot = ColorUtils.remap(dot, 0, 10, 0.1, 1.1);
            // dot = ColorUtils.clamp(dot, -0.5, 1.1);
            // dot **=2
            dot = ColorUtils.clamp(dot, 0.0, 1);
            //console.log(dot);
            color = ColorUtils.hsv(this.hsv[0], this.hsv[1], this.hsv[2] * dot);
            //console.log(color);

        }
        //console.log(new_color);
        return color;
    }
}

module.exports = ExpandingRing;

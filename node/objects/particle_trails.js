
const CObject = new require('./objects');

const ColorUtils = new require('../lib/color_utils');
const MathUtils = new require('../lib/math_utils');

class ParticleTrails extends CObject {

    constructor() {

        super();

        this.name = "ParticleTrails";
        this.particles = [];
        this.numParticles = 200;
    }

    random_ttl() {
        this.ttl = ColorUtils.remap(Math.random(), 0, 1, 15000, 30000);
        console.log(this.ttl)
    }

    move(dt) {
        if (this.alive) {
            this.ttl -= dt;
            let factor = dt / 1000.0;
            this.size += factor;
            let time = 0.002 * new Date().getTime();
            for (let i = 0; i < this.numParticles; i++) {
                let s = i / this.numParticles;

                let radius = 0.2 + 1.5 * s;
                let theta = time + 0.04 * i;
                let x = radius * Math.cos(theta);
                let y = radius * Math.sin(theta + 10.0 * Math.sin(theta * 0.15));
                let hue = time * 0.01 + s * 0.2;

                this.particles[i] = {
                    point: [x, 0, y],
                    intensity: 0.2 * s,
                    falloff: 60,
                    color: ColorUtils.hsv(hue, 0.5, 0.8)
                };
                if (this.ttl < 1000) {
                    this.particles[i].color[2] -= 2*factor;
                }
            };


        }
        this.alive = this.ttl > 0;
    }

    draw(coord) {
        // returns an rgb tuple to add to the current coordinates color

        let r = 0;
        let g = 0;
        let b = 0;

        for (let i = 0; i < this.particles.length; i++) {
            let particle = this.particles[i];

            // Particle to sample distance
            let dx = (coord[0] - particle.point[0]) || 0;
            let dy = (coord[1] - particle.point[1]) || 0;
            let dz = (coord[2] - particle.point[2]) || 0;
            let dist2 = dx * dx + dy * dy + dz * dz;


            // Particle edge falloff
            let intensity = particle.intensity / (1 + particle.falloff * dist2);

            // Intensity scaling
            r += particle.color[0] * intensity;
            g += particle.color[1] * intensity;
            b += particle.color[2] * intensity;
        }

        return [r, g, b];



    }
}

module.exports = ParticleTrails;

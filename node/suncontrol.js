#!/usr/bin/env node

var OPC = new require('./opc');
var model = OPC.loadModel(process.argv[2] || '../layouts/grid32x16z.json');
var client = new OPC('localhost', 7890);


const CObject = new require('./objects/objects.js');
const ExpandingBall = new require('./objects/expanding_ball.js');
const JuliaSet = new require('./objects/julia.js');


var min = Math.min;
var max = Math.max;
var sin = Math.sin;
var cos = Math.cos;
var pow = Math.pow;
var sqrt = Math.sqrt;


var world = {
    time: 0,
    boundary: [],
    objects: []
};


var start_time;
var boundary;


function compute_boundary(model) {
    let min_x = 0.0;
    let min_y = 0.0;
    let max_x = 0.0;
    let max_y = 0.0;
    let min_z = 0.0;
    let max_z = 0.0;

    model.forEach(function (p) {
        let x = p.point[0];
        let y = p.point[1];
        let z = p.point[2];

        min_x = min(x, min_x);
        min_y = min(y, min_y);
        min_z = min(z, min_z);
        max_x = max(x, max_x);
        max_y = max(y, max_y);
        max_z = max(z, max_z);
    });

    let min_coord = [min_x, min_y, min_z];
    let max_coord = [max_x, max_y, max_z];
    bound = [min_coord, max_coord];
    return bound;
}

function chooseShape(world) {
    let obj;
    // return new JuliaSet();
    let julia_objects = world.objects.filter(function (obj) {
        return obj.name == "JuliaSet";
    });

    if (julia_objects.length == 0 && Math.random() > 0.9) {
        console.log("spawning Julia Set")
        obj = new JuliaSet();
    } else if (Math.random() > 0.2) {
        obj = new ExpandingBall();
    } else {
        obj = new CObject()
    }
    return obj;
}

function update_world(t) {
    let last_time = world['time'];
    let delta_t = t - last_time;
    // console.log("update:", delta_t);
    world.time = t;
    world.hue = (world.hue += 0.001) % 1;

    let objects = world['objects'];

    objects.forEach(function (obj) {
        obj.move(delta_t);
    });

    new_objects = objects.filter(function (obj) {
        return obj.alive
    });

    if (new_objects.length < 6 && Math.random() > 0.9) {
        console.log('new object', new_objects.length);
        let obj = chooseShape(world);
        world.hue += 0.05;
        obj.init_random({boundary: world['boundary'], primary: world.hue});
        new_objects.push(obj);
    }

    world.objects = new_objects;
}

var i = 0;

function draw() {
    i += 1;
    const ns = process.hrtime();
    var now = new Date().getTime();
    let t = now - start_time;
    update_world(t, world);

    function shader(p) {
        let r = 0.0, g = 0.0, b = 0.0;

        world.objects.forEach(function (obj) {
            let new_color = obj.draw(p.point);
            r += new_color[0];
            g += new_color[1];
            b += new_color[2];
        });
        //console.log(p);
        // console.log("rgb:", r, g, b);
        return [r, g, b];
    }

    client.mapPixels(shader, model);
    const nsthen = process.hrtime();
    console.log((nsthen[1] - ns[1]) / 1000, 'mus');

}

function frameCount() {
    let time = new Date().getTime() / 1000;
    console.log("###### :", i, time);
}

start_time = new Date().getTime();
boundary = compute_boundary(model);
world['boundary'] = boundary;
world.hue = 0;

setInterval(draw, 30);
// setInterval(frameCount, 1000);
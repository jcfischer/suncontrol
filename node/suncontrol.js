#!/usr/bin/env node

var OPC = new require('./opc');
var model = OPC.loadModel(process.argv[2] || '../layouts/grid32x16z.json');
var client = new OPC('localhost', 7890);


const CObject = new require('./objects');


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

    model.forEach(function(p) {
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

function update_world(t) {
    let last_time = world['time'];
    let delta_t = t - last_time;
     // console.log("update:", delta_t);
    let new_world = {
        time: t,
        boundary: world['boundary'],
        objects: []
    };
    let objects = world['objects'];

    objects.forEach(function(obj) {
        obj.move(delta_t);
    });

    new_objects = objects.filter(function(obj) { return obj.alive });

    if (new_objects.length < 6 && Math.random() > 0.9) {
        console.log('new object', new_objects.length);
        let obj = new CObject();
        obj.init_random(world['boundary']);
        new_objects.push(obj);
    }

    new_world['objects'] = new_objects;
    world = new_world;
}

function draw() {

    var now = new Date().getTime();
    let t = now - start_time;
    update_world(t, world);

    function shader(p) {
            let r = 0.0, g = 0.0, b = 0.0;

            world.objects.forEach( function (obj) {
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
}

start_time = new Date().getTime();
boundary = compute_boundary(model);
world['boundary'] = boundary;

setInterval(draw, 25);
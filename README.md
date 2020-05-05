# Suncontrol

Python scripts to control a 3-dimensional structure of WS2812b LEDs. 
Using the Adafruit [Fadecandy](https://www.adafruit.com/product/1689) to
control the individual LEDs.

This repositories copies codes from the [Fadecandy](https://github.com/scanlime/fadecandy) and the 
[Openpixelcontrol](https://github.com/zestyping/openpixelcontrol)
repositories.

## Installation

Uses Python 3.6.5 (via [Pyenv](https://github.com/pyenv/pyenv))

This repository probably only works under OS X as it doesn't contain the Linux and Windows
binaries / libraries.


## Running

Open two terminal windows to run the server and the actual program.

### Server

For development, run `gl_server`:

    $ bin/gl_server -l layouts/sunmachines.json
    
when connected to Hardware, run `fcserver-osx`  

    $ bin/fcserver-osx bin/sunmachines.json
    
The `sunmachiens.json` file contains the layout of the LEDs (in the `layouts` directory) or
the `fcserver` configuration (there are currently 5 strands of 50 LEDs each connected to the
Fadecandy)

### Control Program

Run the python program:

    $ python python/experiments.py --layout layouts/sunmachines.json
    
or the node version

    $ cd node
    $ node suncontrol.js ../layouts/sunmachines.json

  



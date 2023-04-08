#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import struct
import time
import sys

# Reading raw keyboard input from /dev/input, see:
# https://stackoverflow.com/questions/5060710/format-of-dev-input-event


# Create your objects here.
ev3 = EV3Brick()

device="/dev/input/event2"

# Read keyboard event codes from keyMap
keysIn=open("keyMap", "r")
kbdCodes={}
for line in keysIn:
    # Split the line on whitespace
    sp=line.split()
    
    # Ensure there are at least 2 things on the line
    if(len(sp)>=2):
        if(sp[0].startswith("KEY_")):
            key=sp[0]
            # The code may not be valid hex, ignore
            try:
                code=int(sp[1],0)
                #print("Keycode {} to {}".format(code, key))
                kbdCodes[code]=key
            except:
                pass


"""
FORMAT represents the format used by linux kernel input event struct
See https://github.com/torvalds/linux/blob/v5.5-rc5/include/uapi/linux/input.h#L28
Stands for: long int, long int, unsigned short, unsigned short, unsigned int
"""
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

#open file in binary mode
in_file = open(device, "rb")

event = in_file.read(EVENT_SIZE)

print("Starting keyboard test....")

while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

    if type==1 and value==1:
        # We should have a keycode mapping for this, but use try, just in case
        try:
            key=kbdCodes[code]
        except:
            key="NONE"
        print(key,"pressed")

    # Lets try something with the brick, beep on a B
    if(key=="KEY_B"):
        ev3.speaker.beep()

    event = in_file.read(EVENT_SIZE)

in_file.close()

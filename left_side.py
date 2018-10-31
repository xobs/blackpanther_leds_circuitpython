# Note, this version ONLY works with the lift rib version
import sys
import os

import random
import board
import neopixel

import time

import board
import math

import digitalio
from digitalio import DigitalInOut, Direction, Pull

leds = {
    "left_rib": {
        "data_pin": board.A7,
        "num_pixels": 8,
        "order": neopixel.GRB,
        "brightness_lvl": 0.2,
        "led_object": None,
    },
    "left_chest": {
        "data_pin": board.NEOPIXEL,
        "num_pixels": 10,
        "order": neopixel.GRB,
        "brightness_lvl": 0.2,
        "led_object": None,
    },
    "left_abs": {
        "data_pin": board.A2,
        "num_pixels": 8,
        "order": neopixel.GRB,
        "brightness_lvl": 0.2,
        "led_object": None,
    },
    # "left_middle": {},

    # "right_rib": {},
    # "right_chest": {},
    # "right_abs": {},
    # "right_middle": {},
}




DEBUG_MODE = False
MAX_NUMBER_OF_ANIMATION_STATES = 5

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
left_rib_data_pin = board.A7

# The number of NeoPixels
left_rib_num_pixels = 8

# Disable this when not running on indiviual test strip
num_pixels = left_rib_num_pixels

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
BRIGHTNESS_LVL = 0.2

# Initialize NeoPixel object for left rib
left_rib_pixel_strip = neopixel.NeoPixel(
    left_rib_data_pin,
    left_rib_num_pixels,
    brightness=BRIGHTNESS_LVL,
    auto_write=False,
    pixel_order=ORDER,
)

# TESTING ONLY:
pixels = left_rib_pixel_strip

# source: http://blender.stackexchange.com/questions/1879/is-it-possible-to-dump-an-objects-properties-and-methods

# NOTE: Use this guy to initialize neopixel objects and add them to our dictonary lookup
def create_neopixel_objects(device=None):
    # if device object exists
    if device in leds:
        _neopixel_obj = neopixel.NeoPixel(
            leds[device]["data_pin"],
            leds[device]["num_pixels"],
            brightness=leds[device]["brightness_lvl"],
            auto_write=False,
            pixel_order=leds[device]["order"],
        )

        # Add neopixel object to dict
        leds[device]["led_object"] = _neopixel_obj

# TODO: Add the other devices
# SETUP
create_neopixel_objects(device="left_rib")

# OLD VALUES
# DEBUG_MODE = False
# MAX_NUMBER_OF_ANIMATION_STATES = 5
DEBUG_MODE = False
MAX_NUMBER_OF_ANIMATION_STATES = len(leds)

def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


def _delay(time_in_seconds):
    """[Perform a time sleep in miliseconds.]

    Arguments:
        time_in_seconds {[int]} -- [delay ammount, in seconds. Function automatically converts it to miliseconds]
    """

    to_ms = float(time_in_seconds / 1000)
    time.sleep(to_ms)

# FIXME: add argument device=None
def _showStrip(device=None):
    """[Arduino version of showStrip, taken from tweaking4all]

    Arguments:
        component {ANY} -- [EG. NeoPixel object, like 'left_rib_pixel_strip']
    """
    # Get device object (Usually of type NeoPixel)
    device = leds[device]["led_object"]
    device.show()

# FIXME: add argument device=None
def _setPixel(position, r, g, b, device=None):
    """[Arduino version of setPixel(), taken from tweaking4all]

    Arguments:
        position {int} -- [description]
        r {int} -- [description]
        g {int} -- [description]
        b {int} -- [description]
    """
    if DEBUG_MODE:
        print("INSIDE: _setPixel: r={}, g={}, b={}".format(r, g, b))

    if type(r) == float:
        r = int(r)

    if type(b) == float:
        b = int(b)

    if type(g) == float:
        g = int(g)

    _rgb = (r, g, b) if leds[device]["order"] == neopixel.RGB or leds[device]["order"] == neopixel.GRB else (
        r, g, b, 0)

    pixels = leds[device]["led_object"]
    pixels[position] = _rgb
    # time.sleep(0.1)

# FIXME: add argument device=None
def _setAll(r, g, b, device=None):
    """[Arduino version of setAll(), taken from tweaking4all]

    Arguments:
        r {[type]} -- [description]
        g {[type]} -- [description]
        b {[type]} -- [description]
    """

    num_pixels = leds[device]["num_pixels"]

    for i in range(num_pixels):
        _setPixel(i, r, g, b, device=device)
    _showStrip(device=device)


def shortkeypress(color_palette):
    color_palette += 1

    if color_palette > MAX_NUMBER_OF_ANIMATION_STATES:
        color_palette = 1

    return color_palette

# FIXME: add argument device=None
def _RunningLights(red, green, blue, WaveDelay):
    """[summary]

    Arguments:
        red {int} -- [hex representation of color red]
        green {int} -- [hex representation of color green]
        blue {int} -- [hex representation of color blue]
        WaveDelay {int} -- [time to delay animation, in seconds (will be converted to miliseconds)]
    """

    position = 0

    i = 0

    # FIXME: replace num_pixels with leds[device]["num_pixels"]
    DOUBLE_NUM_PIXELS = num_pixels * 2

    while i < DOUBLE_NUM_PIXELS:
        if DEBUG_MODE:
            print("INSIDE: _RunningLights FIRST LOOP: i={}".format(i))
        position = position + 1  # = 0; #Position + Rate;

        j = 0
        # FIXME: replace num_pixels with leds[device]["num_pixels"]
        while j < num_pixels:
            # NOTE: From orig
            # sine wave, 3 offset waves make a rainbow!
            # float level = sin(i+Position) * 127 + 128
            # setPixel(i, level, 0, 0)
            # float level = sin(i+Position) * 127 + 128

            r = ((math.sin(j + position) * 127 + 128) / 255) * red
            g = ((math.sin(j + position) * 127 + 128) / 255) * green
            b = ((math.sin(j + position) * 127 + 128) / 255) * blue

            if DEBUG_MODE:
                print(
                    "INSIDE: _RunningLights SECOND LOOP: r={}, g={}, b={}".format(r, g, b))

            # FIXME: add argument device=device
            _setPixel(
                j,
                r,
                g,
                b,
            )

            j = j + 1

        # FIXME: add argument device=device
        _showStrip()
        _delay(WaveDelay)
        i = i + 1


def _colorWipe(red, green, blue, WaveDelay):
    """[ColorWipe animation from tweaking4all]
    """
    k = 0
    while k < num_pixels:
        if DEBUG_MODE:
            print("BEFORE - INSIDE: _colorWipe FIRST LOOP: k={}".format(k))
            print(
                "BEFORE - INSIDE: _colorWipe FIRST LOOP: red={}, green={}, blue={}".format(
                    red, green, blue
                )
            )

        # FIXME: add argument device=device
        _setPixel(
            k,
            red,
            green,
            blue,
        )

        # FIXME: add argument device=device
        _showStrip()
        _delay(WaveDelay)

        k = k + 1

# meteorRain - Color (red, green, blue), meteor size, trail decay, random trail decay (true/false), speed delay


def _meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, speedDelay):
    _setAll(0, 0, 0)

    DOUBLE_NUM_LEDS = num_pixels+num_pixels

    i = 0
    while i < DOUBLE_NUM_LEDS:

        # fade brightness all LEDs one step
        j = 0
        while j < num_pixels:
            if (not meteorRandomDecay) or (random.randint(0, 10) > 5):
                _fadeToBlack(j, meteorTrailDecay)
            j = j + 1

        # draw meteor
        j = 0
        while j < meteorSize:
            if (i-j < num_pixels) and (i-j >= 0):
                # FIXME: add argument device=device
                _setPixel(i-j, red, green, blue)
            j = j + 1

        # FIXME: add argument device=device
        _showStrip()
        _delay(speedDelay)
        i = i + 1


def _fadeToBlack(ledNo, fadeValue):
    oldColor = pixels[ledNo]

    # What do 0LL or 0x0UL mean?
    # SOURCE: https://stackoverflow.com/questions/7036056/what-do-0ll-or-0x0ul-mean
    r = float(oldColor[0])
    g = float(oldColor[1])
    b = float(oldColor[2])

    if DEBUG_MODE:
        print(
            "INSIDE: _fadeToBlack r,g,b as floats: r={}, g={}, b={}".format(r, g, b))

    r = (r <= 10) and 0 or int(r-(r*fadeValue/256))
    g = (g <= 10) and 0 or int(g-(g*fadeValue/256))
    b = (b <= 10) and 0 or int(b-(b*fadeValue/256))

    if DEBUG_MODE:
        print(
            "INSIDE: _fadeToBlack r,g,b after conversion: r={}, g={}, b={}".format(r, g, b))

    # FIXME: add argument device=device
    _setPixel(
        ledNo,
        r,
        g,
        b,
    )


# BUTTON REGISTER
button = DigitalInOut(board.BUTTON_A)
button.direction = Direction.INPUT
button.pull = Pull.DOWN
# BUTTON STATES
prevkeystate = False
ledmode = 0  # button press counter, switch color palettes


# dump(board)

# dump(left_rib_data_pin)

# dump(button)

# Mainloop
try:
    while True:

        # FIXME: add argument device=device ( do this for all the ones we want to activate, for every key in dictonary, _showStrip(device=key))
        _showStrip()

        # check for button press
        currkeystate = button.value

        # button press, move to next pattern
        if (prevkeystate is not True) and currkeystate:
            ledmode = shortkeypress(ledmode)

        # save button press state
        prevkeystate = currkeystate

        # STATE: black panther solid colors on
        if ledmode == 1:
            _setAll(141, 0, 155)

        # STATE: BP Running purple lights
        elif ledmode == 2:
            _RunningLights(141, 0, 155, 50)

        # STATE: ColorWipe Purple
        elif ledmode == 3:
            _colorWipe(141, 0, 155, 50)
            _colorWipe(0, 0, 0, 50)

        # STATE: MeteorRain
        # meteorRain - Color (red, green, blue), meteor size, trail decay, random trail decay (true/false), speed delay
        elif ledmode == 4:
            _meteorRain(141, 0, 155, 10, 64, True, 30)

        # STATE: OFF
        elif ledmode == 5:
            _setAll(0, 0, 0)

        time.sleep(0.01)

except KeyboardInterrupt:
    pass

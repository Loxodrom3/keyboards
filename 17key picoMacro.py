# Jon Proctor April 2021  - PCB v03 submitted
# Prototype for using Rasp Pi Pico for Macro HID
# https://learn.adafruit.com/diy-pico-mechanical-keyboard-with-fritzing-circuitpython/code-the-pico-keyboard
# https://github.com/adafruit/Adafruit_CircuitPython_HID
# KeyCodes: https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/master/adafruit_hid/keycode.py
# Consumer Controls: https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/master/adafruit_hid/consumer_control_code.py
# using 1 GPIO for 1 button (Switch) Not using a matrix for keyboard

import time
import digitalio
import board
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# NeoPixels SetUp
neo_pin = board.GP28
numPixels = 17
ORDER = neopixel.GRB
keyLED = neopixel.NeoPixel(neo_pin, numPixels, brightness=0.50, auto_write=False, pixel_order=ORDER)
offset = 0

# for i in range(0, numPixels, 1):
#    keyLED[i] = (0, 0, 50)
keyLED[0] = (0, 0, 50)
keyLED.show()
time.sleep(0.3)

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

pins = [
    board.GP27,
    board.GP26,
    board.GP22,
    board.GP21,
    board.GP20,
    board.GP19,
    board.GP18,
    board.GP17,
    board.GP16,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP13,
    board.GP12,
    board.GP11,
    board.GP10,
    board.GP14
]

MEDIA = 1
KEY = 2

keymap = {
    (0):  (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.ONE)),  # OBS: Ctrl+ALT+1 Transition
    (1):  (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.TWO)),  # OBS: Ctrl+2 Switch to scene - Just Jon
    (2):  (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.THREE)),# OBS: Ctrl+3 Switch to scene - Screen 2
    (3):  (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.FOUR)), # OBS: Ctrl+4 Switch to scene - Screen 2 with pi inset

    (4):  (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.FIVE)), # OBS: Ctrl+5 Switch to scene - Cam2 Cam1
    (5):  (KEY, (Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.SIX)),  # OBS: Ctrl+6 Switch to scene - Cam1 Cam25
    (6):  (MEDIA, ConsumerControlCode.MUTE),  # Media Mute
    (7):  (MEDIA, ConsumerControlCode.VOLUME_DECREMENT), # Media Volume Down

    (8):  (MEDIA, ConsumerControlCode.VOLUME_INCREMENT), # Media Volume Up
    (9):  (MEDIA, ConsumerControlCode.VOLUME_INCREMENT), # Media Volume Up
    (10): (KEY, [Keycode.W]), # no switch
    (11): (KEY, [Keycode.X]), # no switch
    (12): (KEY, [Keycode.Y]), # no switch
    (13): (KEY, [Keycode.Z]), # no switch

    (14): (KEY, [Keycode.I]), # no switch
    (15): (KEY, [Keycode.O]), # no switch
    (16): (KEY, [Keycode.LEFT_ARROW]), # no switch

}
switches = [0,   1,  2,  3,
            4,   5,  6,  7,
            8,   9, 10, 11,
            12, 13, 14, 15,
            16]

for i in range(0, len(switches),1):
    switches[i] = digitalio.DigitalInOut(pins[i])
    switches[i].direction = digitalio.Direction.INPUT
    switches[i].pull = digitalio.Pull.UP

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

clrRed = (200, 0, 0)
clrGrn = (0, 50, 0)
clrPur = (100, 0, 100)
clrBkg = (33, 0, 200)
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for k in range(numPixels):
            pixel_index = (k * 256 // numPixels) + j
            keyLED[k] = wheel(pixel_index & 255)
        keyLED.show()
        time.sleep(wait)

while True:
    for button in range(0, len(switches), 1):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                    else:
                        cc.send(keymap[button][1])
                except ValueError:  # deals w six key limit
                    pass
                switch_state[button] = 1
        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])
                except ValueError:
                    pass
                switch_state[button] = 0

    print(switch_state)
    for i in range(0, len(switches), 1):
        if switches[i].value:
            keyLED[i+offset]=(clrBkg)
        else:
            keyLED[i+offset]=(clrRed)
    keyLED.show()
    time.sleep(0.01)  # debounce

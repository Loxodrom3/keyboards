# Jon Proctor April 2021  - PCB v03 submitted
# Prototype for using Rasp Pi Pico as a Midi controller
# Using this Adafruit project for inspiration
# https://learn.adafruit.com/raspberry-pi-pico-led-arcade-button-midi-controller-fighter
# using 1 GPIO for 1 button (Switch) Not using a matrix for keyboard

import usb_hid
import neopixel

import time
import board
import displayio
import terminalio
import adafruit_aw9523
import busio
import adafruit_ssd1327
import digitalio
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
import usb_midi
import adafruit_midi
from adafruit_midi.note_on          import NoteOn
from adafruit_midi.note_off         import NoteOff



# NeoPixels SetUp
neo_pin = board.GP28
numPixels = 17
ORDER = neopixel.GRB
keyLED = neopixel.NeoPixel(neo_pin, numPixels, brightness=0.50, auto_write=False, pixel_order=ORDER)
offset = 0

for i in range(0, numPixels, 1):
    keyLED[i] = (100, 0, 0)
keyLED.show()
time.sleep(0.333)

for i in range(0, numPixels, 1):
    keyLED[i] = (0, 100, 0)
keyLED.show()
time.sleep(0.333)

for i in range(0, numPixels, 1):
    keyLED[i] = (0, 0, 100)
keyLED.show()
time.sleep(0.333)


note_pins = [
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


switches = [0,   1,  2,  3,
            4,   5,  6,  7,
            8,   9, 10, 11,
            12, 13, 14, 15]

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

clrRed = (200, 0, 0)
clrGrn = (0, 50, 0)
clrPur = (100, 0, 100)
clrBkg = (33, 0, 200)

# ---------------------------
# i2c setup, higher frequency for display refresh
# i2c = busio.I2C(board.GP1, board.GP0, frequency=1000000)
#  i2c display setup
# display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)
#  i2c AW9523 GPIO expander setup
# aw = adafruit_aw9523.AW9523(i2c)
#  MIDI setup as MIDI out device
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

#  button pins, all pins in order skipping GP15
note_pins = [
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
    board.GP10
]
 
note_buttons = []
 
for pin in note_pins:
    note_pin = digitalio.DigitalInOut(pin)
    note_pin.direction = digitalio.Direction.INPUT
    note_pin.pull = digitalio.Pull.UP
    note_buttons.append(note_pin)

#  note states
note0_pressed = False
note1_pressed = False
note2_pressed = False
note3_pressed = False
note4_pressed = False
note5_pressed = False
note6_pressed = False
note7_pressed = False
note8_pressed = False
note9_pressed = False
note10_pressed = False
note11_pressed = False
note12_pressed = False
note13_pressed = False
note14_pressed = False
note15_pressed = False

#  array of note states
note_states = [note0_pressed, note1_pressed, note2_pressed, note3_pressed,
               note4_pressed, note5_pressed, note6_pressed, note7_pressed,
               note8_pressed, note9_pressed, note10_pressed, note11_pressed,
               note12_pressed, note13_pressed, note14_pressed, note15_pressed]

#  array of default MIDI notes
midi_notes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]



while True:
    #  MIDI input
    for i in range(16):
        buttons = note_buttons[i]
        #  if button is pressed...
        if not buttons.value and note_states[i] is False:
            #  send the MIDI note and light up the LED
            midi.send(NoteOn(midi_notes[i], 120))
            note_states[i] = True
            keyLED[i] = (clrRed)
            keyLED.show()
        #  if the button is released...
        if buttons.value and note_states[i] is True:
            #  stop sending the MIDI note and turn off the LED
            midi.send(NoteOff(midi_notes[i], 120))
            note_states[i] = False
            keyLED[i] = (clrBkg)
            keyLED.show()





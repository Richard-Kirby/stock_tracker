import time

import scrollphathd
from scrollphathd.fonts import (fontd3, fontgauntlet, fontorgan, fonthachicro, font3x5, font5x5, font5x7,
                                font5x7smoothed, fontd3)
import smbus

""" *** This uses additional I2C channels to drive the extra displays. 
** this enables the channel 0 /boot/firmware/config.txt
dtparm= i2cvc=on

** this adds bus 3 in /boot/firmware/config.txt ****SDA is pin 17, *SCL is pin 27*
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=17,i2c_gpio_scl=27

** this adds bus 4 in /boot/firmware/config.txt ****SDA is pin 23, *SCL is pin 24*
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24

"""

print("""
Scroll pHAT HD: Simple Scrolling

A simple example showing a basic scrolling loop for scrolling
single messages across the display.

Press Ctrl+C to exit.
""")

def scroll_message(font, message):
    scrollphathd.set_font(font)
    scrollphathd.clear()                         # Clear the display and reset scrolling to (0, 0)
    length = scrollphathd.write_string(message)  # Write out your message
    scrollphathd.show()                          # Show the result
    time.sleep(0.5)                              # Initial delay before scrolling

    length -= scrollphathd.width

    # Now for the scrolling loop...
    while length > 0:
        scrollphathd.scroll(1)                   # Scroll the buffer one place to the left
        scrollphathd.show()                      # Show the result
        length -= 1
        time.sleep(0.05)                         # Delay for each scrolling step

    time.sleep(0.5)                              # Delay at the end of scrolling


class ScrollDisplay:
    def __init__(self, i2c_channel, brightness=1.0, rotation=0):
        self.i2c_channel = smbus.SMBus(i2c_channel)
        self.brightness = brightness
        self.rotation = rotation

    def scroll_message(self, font, message):
        scrollphathd.display = None
        scrollphathd.setup(i2c_dev=self.i2c_channel)
        scrollphathd.set_brightness(self.brightness)
        scrollphathd.rotate(self.rotation)

        print(scrollphathd.display)
        scroll_message(font, message)

    def scroll_message(self, font, message):
        scrollphathd.display = None
        scrollphathd.setup(i2c_dev=self.i2c_channel)
        scrollphathd.set_brightness(self.brightness)
        scrollphathd.rotate(self.rotation)

        print(scrollphathd.display)
        scroll_message(font, message)


displays = [(0, "0 disp 0", 0),
            (1, "1 disp 1", 0),
            (3, "3 disp 3", 0),
            (4, "4 disp 4", 0)]

if __name__ == '__main__':

    while True:
        for display in displays:
            try:
                print(display[1])
                scroll_display0 = ScrollDisplay(display[0], rotation = display[2])
                scroll_display0.scroll_message(font5x7, display[1])
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)

        


"""
for font, text in (
        #(fontgauntlet, "THIS IS FONT GAUNTLET"),
        # (fontorgan, "THIS IS FONT ORGAN"),
        # (fonthachicro, "This is font Hachicro"),
        (font3x5, "This is font 3x5"),
        #(font5x5, "This is font 5x5"),
        (font5x7, "This is font 5x7"),
        #(font5x7smoothed, "This is font 5x7 smoothed")
):
        #(fontd3, "This is font d3")):

    # scroll_message(font, text)
    # time.sleep(0.5)
    scroll_message(font, "RPI 619.00 -21.00")
    time.sleep(0.5)
"""


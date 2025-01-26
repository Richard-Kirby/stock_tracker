import time
import threading
import queue 

import scrollphathd
from scrollphathd.fonts import (fontd3, fontgauntlet, fontorgan, fonthachicro, font3x5, font5x5, font5x7,
                                font5x7smoothed, fontd3)
import smbus

""" *** This uses additional I2C channels to drive the extra testdisplays. 
** this enables the channel 0 /boot/firmware/config.txt
dtparm= i2cvc=on

** this adds bus 3 in /boot/firmware/config.txt ****SDA is pin 17, *SCL is pin 27*
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=17,i2c_gpio_scl=27

** this adds bus 4 in /boot/firmware/config.txt ****SDA is pin 23, *SCL is pin 24*
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24

"""


# Class to manage a Pimoroni scroll HD disp. 
class ScrollDisplay:
    def __init__(self, i2c_channel, brightness=1.0, rotation=0):
        self.i2c_channel = smbus.SMBus(i2c_channel)
        self.brightness = brightness
        self.rotation = rotation
        
    # Set the disp to use. This is needed as the library only handles a single disp. 
    # ToDo: make this work better. Should be able to split the time between the testdisplays so they can work in parallel. 
    def set_display(self):
        scrollphathd.disp = None
        scrollphathd.setup(i2c_dev=self.i2c_channel)
        scrollphathd.set_brightness(self.brightness)
        scrollphathd.rotate(self.rotation)

    # Write a message - no scrolling. 
    def write_message(self, font, message):
        self.set_display()
        # print(f"message {message}")
        scrollphathd.set_font(font)
        scrollphathd.clear()                         # Clear the disp and reset scrolling to (0, 0)
        scrollphathd.write_string(message)  # Write out your message
        # print(f"message length {length}")
        scrollphathd.show()                          # Show the result
        time.sleep(0.5)

    # Scroll the message.
    def scroll_message(self, font, message):
        scrollphathd.disp = None
        scrollphathd.setup(i2c_dev=self.i2c_channel)
        scrollphathd.set_brightness(self.brightness)
        scrollphathd.rotate(self.rotation)

        scrollphathd.set_font(font)
        scrollphathd.clear()  # Clear the disp and reset scrolling to (0, 0)
        length = scrollphathd.write_string(message)  # Write out your message
        scrollphathd.show()  # Show the result
        time.sleep(0.25)  # Initial delay before scrolling

        length -= scrollphathd.width

        # Now for the scrolling loop...
        while length > 0:
            scrollphathd.scroll(1)  # Scroll the buffer one place to the left
            scrollphathd.show()  # Show the result
            length -= 1
            time.sleep(0.01)  # Delay for each scrolling step

        time.sleep(0.25)

# Display Manager - manages the multiple testdisplays as needed. 
class DisplayManager(threading.Thread):
    def __init__(self, display_configs):
        threading.Thread.__init__(self)

        # Set up queue to receive messages for the stock dial.
        self.queue = queue.Queue()
        
        displays =[]
        
        for display in display_configs:
            new_display_obj = ScrollDisplay(display["channel"], display["brightness"],  
                                            display["rotation"])
            new_display = {"name": display["name"], "obj":new_display_obj}
            
            displays.append(new_display)
        
        print(displays)

    def run(self):
        pass
        
        


if __name__ == '__main__':

    """
    testdisplays = [(0, "0 disp 0", 0),
                (1, "1 disp 1", 0),
                (3, "3 disp 3", 0),
                (4, "4 disp 4", 0)]

    while True:
        for disp in testdisplays:
            try:
                # print(disp[1])
                scroll_display0 = ScrollDisplay(disp[0], rotation = disp[2], brightness = 0.5)
                scroll_display0.scroll_message(font5x7, disp[1])
                scroll_display0.write_message(font5x7, "RPI")
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)

    """
    test_displays =[]

    test_displays.append ({"name":"bottom_left", "channel": 0, "brightness":0.5, "rotation":0})
    test_displays.append ({"name":"bottom_right", "channel": 1, "brightness":0.5, "rotation":0})
    test_displays.append ({"name":"top_left", "channel": 3, "brightness":0.5, "rotation":0})
    test_displays.append ({"name":"top_right", "channel": 4, "brightness":0.5, "rotation":0})

    display_manager = DisplayManager(test_displays)
    # test_displays{}

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


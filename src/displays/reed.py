import pigpio_start
import RPi.GPIO as GPIO
import pigpio

import sys
import time


# Controls a reed switch, which can be ON (magnet close by) or OFF. Supply pin that connects to the reed switch.
class ReedSwitch:
    def __init__(self, pi, pin):
        self.pi = pi
        self.pi.set_mode(pin, pigpio.INPUT)
        self.pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
        self.pin = pin

    def return_state(self):
        ret = self.pi.read(self.pin)
        return ret


if __name__ == "__main__":
    pi = pigpio.pi()

    while True:
        try:
            reed = ReedSwitch(pi, 4)

            while True:
                print(f"State of reed switch {reed.return_state()}")
                time.sleep(0.01)

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

        finally:
            pi.stop()
            sys.exit()
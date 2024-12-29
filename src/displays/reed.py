import pigpio_start

import pigpio

import time

# Controls a reed switch, which can be ON (magnet close by) or OFF. Supply pin that connects to the reed switch.
class ReedSwitch:
    def __init__(self, pi, pin):
        pi.set_mode(pin, pigpio.INPUT)
        self.pin = pin

    def return_state(self):
        ret = pi.read(self.pin)
        return ret


if __name__ == "__main__":
    pi = pigpio.pi()

    while True:
        try:
            reed = ReedSwitch(pi, 27)
            cw_dir = True

            while True:
                print(f"State of reed switch {reed.return_state()}")
                time.sleep(3)

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

        finally:
            pi.stop()
            sys.exit()
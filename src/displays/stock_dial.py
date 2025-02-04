import threading
import queue
import time

import pigpio
import displays.pigpio_start
from . import stepper
from . import reed


class ZeroException(Exception):
    def __init__(self):
        super().__init__("Could not find zero for some reason. Check Zero Switch function")


# Stock Dial class to physically indicate the stock price, rather than just display it.
class StockDial(threading.Thread):
    def __init__(self, stepper_control, zero_switch, offset):
        threading.Thread.__init__(self)

        # Set up queue to receive messages for the stock dial.
        self.queue = queue.Queue()

        # Stepper motor controller
        self.stepper_control = stepper_control

        # To monitor the zero switch
        self.zero_switch = zero_switch

        # Offset is used to calibrate number of half steps to center of the dial, which will
        # not be aligned exactly with the zero_switch
        self.offset = offset

        # Zero found
        self.zeroed = 0

        self.current_position = None

    # Find the zero point - move in a single direction until the zero switch fires - if it goes too
    # many steps, something must be wrong.
    def seek_zero(self):

        try:

            step_num = 0
            while self.zeroed == 0:

                # print(f"Zeroed?{self.zeroed}")
                self.stepper_control.clockwise_step()

                # Check whether zero has been found yet.
                self.zeroed = self.zero_switch.return_state()
                step_num += 1

                # Zeroing allows the stepper to calibrate
                if self.zeroed == 1:
                    # found the switch, so set current position to the offset
                    self.current_position = self.offset

                    print(f"curr position = {self.current_position}")

                # print(f"Zeroed?{self.zeroed}")

                if step_num > 450:
                    raise ZeroException()

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

    # Goes to the defined position, relative to neutral position (not zero as defined by the reed switch).
    def goto_position(self, cmd_position):

        print(f"Goto position {cmd_position}")
        at_position = False

        while at_position is False:
            # print("get to position")

            error = cmd_position - self.current_position

            if error > 0:
                # print(f"clockwise {error}")
                self.stepper_control.clockwise_step()
                self.current_position += 1

            elif error < 0:
                # print(f"counter clockwise {error}")
                self.stepper_control.counter_clockwise_step()
                self.current_position -= 1

            # error must be zero, so at position is now True.
            else:
                print("at position")
                at_position = True

    def run(self):

        while True:
            target_position = None

            while not self.queue.empty():
                target_position = int(self.queue.get_nowait())

            # print(f"target_position {target_position}")

            if target_position is not None:
                self.goto_position(target_position)

            time.sleep(0.5)


if __name__ == "__main__":
    pi = pigpio.pi()

    # Set up the stepper
    stepper_obj = stepper.StepperMotor(pi, 26, 13, 21, 20, sequence=stepper.HALF_STEP_SEQUENCE,
                                       delay_after_step=0.01)
    # Set up the zero point switch
    zero_switch_obj = reed.ReedSwitch(pi, 4)

    # Create the stock dial.
    stock_dial = StockDial(stepper_obj, zero_switch_obj, 20)

    # Go to zero, then do a few other moves.
    stock_dial.seek_zero()

    stock_dial.start()

    time.sleep(2)
    stock_dial.queue.put_nowait('0')
    time.sleep(2)
    stock_dial.queue.put_nowait('-100')
    time.sleep(2)
    stock_dial.queue.put_nowait('100')

    time.sleep(2)
    stock_dial.queue.put_nowait('0')
    time.sleep(2)
    stock_dial.queue.put_nowait('-50')
    time.sleep(2)
    stock_dial.queue.put_nowait('50')

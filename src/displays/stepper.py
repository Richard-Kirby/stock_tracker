import sys
import time
from collections import deque
import pigpio
import pigpio_start

pi = pigpio.pi()

FULL_STEP_SEQUENCE = (
  (1, 1, 0, 0),
  (0, 1, 1, 0),
  (0, 0, 1, 1),
  (1, 0, 0, 1)
)

HALF_STEP_SEQUENCE = (
  (1, 0, 0, 0),
  (1, 1, 0, 0),
  (0, 1, 0, 0),
  (0, 1, 1, 0),
  (0, 0, 1, 0),
  (0, 0, 1, 1),
  (0, 0, 0, 1),
  (1, 0, 0, 1)
)


class StepperMotor:
    def __init__(self, pi, pin1, pin2, pin3, pin4, sequence=FULL_STEP_SEQUENCE, delay_after_step =0.00015):

        if not isinstance(pi, pigpio.pi):
            raise TypeError("Is not pigpio.pi instance.")

        pi.set_mode(pin1, pigpio.OUTPUT)
        pi.set_mode(pin2, pigpio.OUTPUT)
        pi.set_mode(pin3, pigpio.OUTPUT)
        pi.set_mode(pin4, pigpio.OUTPUT)
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4

        self.pi = pi
        self.delay_after_step = delay_after_step
        self.deque = deque(sequence)

    # Performs the step and waits a period before returning.
    def step_and_delay(self, step):
        self.pi.write(self.pin1, step[0])
        self.pi.write(self.pin2, step[1])
        self.pi.write(self.pin3, step[2])
        self.pi.write(self.pin4, step[3])
        time.sleep(self.delay_after_step)

    # Clockwise step.
    def clockwise_step(self):
        self.deque.rotate(-1)
        self.step_and_delay(self.deque[0])

    # Counterclockwise step
    def counter_clockwise_step(self):
        self.deque.rotate(1)
        self.step_and_delay(self.deque[0])


if __name__ == "__main__":
    while True:
        try:
            stepper = StepperMotor(pi, 26, 13, 21, 20, sequence= HALF_STEP_SEQUENCE,
                                   delay_after_step= 0.1)
            cw_dir = True

            while True:
                for i in range(400):
                    print(f"step cw = {cw_dir}", i)

                    if cw_dir:
                        stepper.clockwise_step()
                    else:
                        stepper.counter_clockwise_step()

                cw_dir = not cw_dir
                time.sleep(3)

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

        finally:
            pi.stop()
            sys.exit()


import threading
import time

import pigpio

from displays import pixel_display, stepper, stock_dial, reed
from interfaces import stock_price_data

from scrollphathd.fonts import (fontd3, fontgauntlet, fontorgan, fonthachicro, font3x5, font5x5, font5x7,
                                font5x7smoothed, fontd3)


class StockTracker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # Stock Tracker has four different displays, set up the list of displays and pass
        # to the display manager, which creates and manages them.

        pixel_displays_list = [{"name": "bottom_left", "channel": 4, "brightness": 0.5, "rotation": 0},
                               {"name": "bottom_right", "channel": 3, "brightness": 0.5, "rotation": 0},
                               {"name": "top_left", "channel": 1, "brightness": 0.5, "rotation": 0},
                               {"name": "top_right", "channel": 0, "brightness": 0.5, "rotation": 0}]

        # Display manager sets up the displays and displays things as needed via a message queue.
        self.display_manager = pixel_display.PixelDisplayManager(pixel_displays_list)
        self.display_manager.start()

        # Set up the Stock Price Dial.
        self.pi = pigpio.pi()

        # Set up the stepper
        stepper_obj = stepper.StepperMotor(self.pi, 26, 13, 21, 20,
                                           sequence=stepper.HALF_STEP_SEQUENCE, delay_after_step=0.01)
        # Set up the zero point switch
        zero_switch_obj = reed.ReedSwitch(self.pi, 4)

        # Create the stock dial.
        self.stock_dial_disp = stock_dial.StockDial(stepper_obj, zero_switch_obj, 20)

        # Go to zero, then do a few other moves.
        self.stock_dial_disp.seek_zero()

        self.stock_dial_disp.start()

        self.ticker_data = stock_price_data.TickerData(['MSFT', 'CSCO',  'GOOG', 'RPI.L'])

    def run(self):

        while True:

            ticker_data_frame = self.ticker_data.get_ticker()

            stock_dict = ticker_data_frame['Close', 'RPI.L'].to_dict()

            # print(stock_dict)

            bottom_price = 700
            top_price = 800
            center = int((top_price - bottom_price)/ 2)

            self.display_manager.queue.put_nowait({"name": 'bottom_left', "font": font3x5, "message": f"{bottom_price}"})
            self.display_manager.queue.put_nowait({"name": 'bottom_right', "font": font3x5, "message": f"{top_price}"})

            for key in stock_dict:
                print(str(key)[:10], str(key)[11:19], f"{stock_dict[key]:.2f}")
                self.display_manager.queue.put_nowait({"name": 'top_left', "font": font3x5, "message": f"{str(key)[11:16]}"})
                self.display_manager.queue.put_nowait({"name": 'top_right', "font": font3x5, "message": f"{stock_dict[key]:.2f}"})

                ratio_bottom_to_top = (stock_dict[key] - bottom_price) / (top_price - bottom_price)

                needle_loc = (ratio_bottom_to_top - 0.5) * 200
                print(f"{needle_loc}")

                print(f"{stock_dict[key]} {top_price} {bottom_price} {ratio_bottom_to_top} {needle_loc}")

                self.stock_dial_disp.queue.put_nowait(int(needle_loc))

                time.sleep(3)

            time.sleep(15)


if __name__ == "__main__":
    stock_tracker = StockTracker()
    stock_tracker.start()

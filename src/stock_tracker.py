import displays


if __name__ == "__main__":
    try:
        stepper = StepperMotor(pi, 26, 13, 21, 20, sequence= halfStepSequence,
                               delayAfterStep = 0.1)
        reed = ReedSwitch(pi, 27)

        cw_dir = True

        while True:
            for i in range(400):
                reed_ret = reed.return_state()
                print(f"step{cw_dir}", i, f"Reed {reed_ret})")

                if cw_dir:
                    stepper.clockwise_step()
                else:
                    stepper.counter_clockwise_step()

                if reed_ret == 1:
                    print("Reed  On")
                    break

            cw_dir = not cw_dir

            time.sleep(3)

    except:
        print("except - Raising")
        raise

    finally:
        pi.stop()
        sys.exit()
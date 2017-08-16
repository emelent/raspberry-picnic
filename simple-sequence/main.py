import sys
sys.path.insert(1, '..')

import time
import lib.pinocchio as pin


LED_RED = 16
LED_YELLOW = 20
LED_GREEN = 21


LEDS = [LED_RED, LED_YELLOW, LED_GREEN]

def setupHw():
    pin.setDebug(False)
    pin.setupHw()
    pin.setupOutPins(LEDS)

def sequence(interval, iterations):
    for i in range(iterations):
        for led in LEDS:
            pin.setOutPinHigh(led)
            time.sleep(interval)
            pin.setOutPinLow(led)

def main():
    setupHw()
    sequence(0.001, 1000)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        pass
    finally:
        print "Quitting..."
        pin.setAllOutPinsLow()
        pin.cleanup()

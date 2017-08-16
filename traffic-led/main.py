import sys
sys.path.insert(1, '..')

import time
import lib.pinocchio as pin

"""
    Simple script to simulate a traffic light
    with 3 L.E.D's and a push button
"""

RED = 16
YELLOW = 20
GREEN = 21

BTN = 18

traffic_lights = [GREEN, YELLOW, RED]
traffic_colors = ["GREEN", "YELLOW", "RED"]

light  = -1 # first light to go on is is (light + 1)%3

def setupHw():
    """
        Setup hardware, gpio pins etc.
    """

    pin.setupHw()
    pin.setupOutPins(traffic_lights)
    pin.setDebug(False)

def nextLight():
    """
        Switch to the next light
    """
    global light
    pin.setAllOutPinsLow()
    light += 1
    light %= len(traffic_lights)
    print traffic_colors[light]
    pin.setOutPinHigh(traffic_lights[light])

def automaticTrafficLight(iterations, interval):
    '''
       Automatic light transitioning to simulate
       traffic light
    '''
    for i in range(iterations):
        for j in range(3):
            nextLight()
            time.sleep(interval)

def manualTrafficLight():
    '''
        Allows for manual transitioning of lights
        to simulate traffic light
    '''
    pin.setupPullUpInPin(BTN)
    print "PUSH BUTTON TO CHANGE LIGHT"
    btn_closed = False
    while True:
        btn_val = pin.getInput(BTN)
        if btn_val and btn_closed:
            nextLight()
            btn_closed = False
        elif not btn_val and not btn_closed:
            btn_closed = True

        time.sleep(0.1)

def main():
    setupHw()
    manualTrafficLight()
    # automaticTrafficLight(2, 2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        pass
        print("Quitting ...")
    finally:
        pin.setAllOutPinsLow()
        pin.cleanup()

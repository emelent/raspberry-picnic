
import sys
sys.path.insert(1, '..')

import time
from random import choice


import lib.pinocchio as pin

"""
    Memory game using an equal amount
    of LED's and push buttons

    Please make sure that your GPIO setup
    is the same as the code before running.
"""

#=====================
# Setup gpio pins
#=====================

BTN_RED = 18
BTN_YELLOW = 23
BTN_GREEN = 24

LED_RED = 16
LED_YELLOW = 20
LED_GREEN = 21

LED_MAP = {
    LED_RED     : "RED",
    LED_YELLOW  : "YELLOW",
    LED_GREEN   : "GREEN"
}

# LED_MAP[LED_RED] = "RED"
# LED_MAP[LED_YELLOW] = "YELLOW"
# LED_MAP[LED_GREEN] = "GREEN"

BTN_MAP = {
    BTN_RED     : LED_RED,
    BTN_YELLOW  : LED_YELLOW,
    BTN_GREEN   : LED_GREEN
}

# BTN_MAP[BTN_RED] = LED_RED
# BTN_MAP[BTN_YELLOW] = LED_YELLOW
# BTN_MAP[BTN_GREEN] = LED_GREEN

#=====================
# In game phrases
#=====================
WIN_PHRASES = [
    "Great job, let's see if you can get the next one!",
    "You got lucky.",
    "Wow, look at you xD.",
    "It only gets harder from here.",
    "Keep it up.",
    "Impossible! No human has ever made it this far.",
    "Looks like we got ourselve's an Einstein over here."
]

LOSS_PHRASES = [
    "Sorry, not this time.",
    "Oops, nice try.",
    "Better luck next time.",
    "You'll have to do a lot better than that",
    "Game Over",
    "Pitiful human, your endeavour ends here.",
    "So close and yet so far.",
    "Well, looks like you've reached your limit."
]
                

def query(msg):
    """
        Output a yes or no query, returns boolean
    """
    r = raw_input("{}(y/n) ".format(msg))
    return r.lower().startswith('y')


def setupHw():
    """
        Setup the hardware
    """
    pin.setDebug(False)
    pin.setupHw()
    pin.setupOutPins(LED_MAP.keys())
    pin.setupPullUpInPins(BTN_MAP.keys())

def getNextSequence(seq_len):
    """
        Randomly generate a light sequence
    """
    return [choice(LED_MAP.keys()) for n in range(seq_len)]

def displaySequence(seq, interval):
    """
        Display sequence
    """
    print "Watch the LED's ==>"
    time.sleep(3)
    for led in seq:
        pin.setOutPinHigh(led)
        time.sleep(interval)
        pin.setOutPinLow(led)
        time.sleep(0.5)
        
def buttonDown(btn_val, btn_closed):
    """
        Check if button has been pressed
    """
    if btn_val and btn_closed:
        return False
    elif not btn_val and not btn_closed:
        return True
    return None


def getPlayerInput(correct_sequence):
    """
        Get push button input from user,
        end game as soon as the user inputs
        the wrong value
    """
    print "Your turn\n"
    count = 0
    btn_closed = {n:False for n in BTN_MAP.keys()}
    seq_len = len(correct_sequence)

    # while user hasn't pushed enough buttons
    while count < seq_len:
        for btn in BTN_MAP.keys():
            btn_val = pin.getInput(btn)
            led = BTN_MAP[btn]
            result = buttonDown(btn_val, btn_closed[btn]) 
            if result:
                # button released
                btn_closed[btn] = True
                pin.setOutPinHigh(led)
                time.sleep(0.3) # keep led on for 0.3 seconds
                pin.setOutPinLow(led)
                if correct_sequence[count] != led:
                    return False
                count += 1
            elif result is False:
                # button released
                btn_closed[btn] = False
                pin.setOutPinLow(led)
        time.sleep(0.1)

    return True

def main():
    """
        Runs game
    """
    setupHw()
    seq_len = 1
    interval = 1
    t1 = t2 = 0 
    bonus_multiplier = 12
    # Main game loop
    while True:
        lvl = 0
        score = 0
        while True:
            print "Level: {}".format(lvl + 1)
            print "Score: {}".format(score) 
            lvl_len = seq_len + int(round(lvl * 1.2))
            seq = getNextSequence(lvl_len)
            displaySequence(seq, interval - (0.1 * lvl))
            t1= time.time()
            if getPlayerInput(seq):
                print choice(WIN_PHRASES)
            else:
                break
            lvl += 1
            t2 = time.time()
            score += seq_len//2 + int(seq_len * (bonus_multiplier/(t2-t1)))

        print choice(LOSS_PHRASES)
        print "Your score was {}.".format(score)
        print
        if not query("Play again?"):
            break


if __name__ == '__main__':
    if not query("Does your GPIO setup match your code?"):
        sys.exit(0)
    try:
        main()
    except KeyboardInterrupt as e:
        pass
    finally:
        print "Quitting..."
        pin.setAllOutPinsLow()
        pin.cleanup()

__doc__ =\
"""
    Wrapper for some common use gpio functions
    meant to make testing GPIO code in the 
    interactive shell a bit less tedious.
"""

#==================================================================
"""
    Hack to override the gpio import with GPIOStub 
    class so any calls do not actually affect the 
    Pi's gpio pins, this is needed because the 
    unittest below is only used to test the logic 
    of the created functions. This is also so the 
    logic tests be performed in a python environment
    without the actual RPi module.
"""
class GPIOStub():
    HIGH = 0
    LOW = 0
    OUT = 0
    IN = 0
    PUD_UP = 0
    PUD_DOWN = 0
    BCM = None

    def output(self, *args, **kwargs):
        pass

    def input(self, *args, **kwargs):
        pass


    def setmode(self, *args, **kwargs):
        pass

    def setwarnings(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass

    def setup(self, *args, **kwargs):
        pass

def hack():
    global gpio
    gpio = GPIOStub()
    print "[Stubbing GPIO]\n"

#==================================================================

try:
    import RPi.GPIO as gpio
except Exception as e:
    hack()


OUT_PINS= {}
IN_PINS = set()
DEBUG = True


def __for_OUT_PINS(pins, f, *args, **kwargs):
    for pin in pins:
        f(pin, *args, **kwargs)

def setupHw():
    """
        Setup hardware, sets gpio mode to BCM
    """
    debugPrint("Setting GPIO to BCM mode")
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

def cleanup():
    debugPrint("Cleaning up...");
    gpio.cleanup()

def setDebug(b):
    """
        Toggle debug output
    """
    global DEBUG
    DEBUG = b

def debugPrint(msg):
    """
        Prints msg if DEBUG is set to True
    """
    if DEBUG:
        print("[DEBUG] {}".format(msg))

def setupOutPin(pin):
    """
        Sets up pin as gpio.OUT
    """
    debugPrint("Setting up outpin {}".format(pin))
    gpio.setup(pin, gpio.OUT)
    OUT_PINS[pin] = False

def setupOutPins(pins):
    """
        Sets multiple pins
    """
    for pin in pins:
        setupOutPin(pin)

def setupPullUpInPin(pin):
    """
        Sets up pin as IN using internal pull-up resistor
    """
    debugPrint("Setting up pud_inpin {}".format(pin))
    gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_UP)
    IN_PINS.add(pin)

def setupPullDownInPin(pin):
    """
        Sets up pin as IN using internal pull-down resistor
    """
    debugPrint("Setting up pud_inpin {}".format(pin))
    gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    IN_PINS.add(pin)

def setupPullUpInPins(pins):
    for pin in pins:
        setupPullUpInPin(pin)

def setupPullDownInPins(pins):
    for pin in pins:
        setupPullDownInPin(pin)

def toggleOutPin(pin):
    """
        Toggle the state of a gpio outpin between HIGH and LOW
    """
    OUT_PINS[pin] = not OUT_PINS[pin]
    if OUT_PINS[pin]:
        setOutPinHigh(pin)
    else:
        setOutPinLow(pin)

def getOutPinState(pin):
    """
        Get the state of a gpio outpin as boolean value
    """
    if checkOutPin(pin):
        return OUT_PINS[pin]
    return None

def getInput(pin):
    """
        Get input from gpio input pin
    """
    if checkInPin(pin):
        return gpio.input(pin)
    return None

def checkOutPin(pin):
    """
        Checks if a output pin is setup
    """
    if pin in OUT_PINS.keys():
        return True
    debugPrint("outpin {} has not been set up")
    return False

def checkInPin(pin):
    """
        Checks if a input pin is setup
    """
    if pin in IN_PINS:
        return True
    debugPrint("inpin {} has not been set up")
    return False

def setOutPinHigh(pin):
    """
        Set output pin to HIGH
    """
    if checkOutPin(pin):
        OUT_PINS[pin] = True
        gpio.output(pin, gpio.HIGH)
        debugPrint("outpin {} -> {}".format(pin, OUT_PINS[pin]))

def setOutPinLow(pin):
    """
        Set output pin to LOW
    """
    if checkOutPin(pin):
        gpio.output(pin, gpio.LOW)
        OUT_PINS[pin] = False
        debugPrint("outpin {} -> {}".format(pin, OUT_PINS[pin]))

def setAllOutPinsLow():
    setOutPinsLow(OUT_PINS.keys())

def setAllOutPinsHigh():
    setOutPinsHigh(OUT_PINS.keys())

def toggleAllOutPins():
    toggleOutPins(OUT_PINS.keys())

def toggleOutPins(pins):
    __for_OUT_PINS(pins, toggleOutPin)

def setOutPinsLow(pins):
    __for_OUT_PINS(pins, setOutPinLow)

def setOutPinsHigh(pins):
    __for_OUT_PINS(pins, setOutPinHigh)

def query(msg):
    """
        Output a yes or no query, returns boolean
    """
    r = raw_input("{}(y/n) ".format(msg))
    return r.lower().startswith('y')




if __name__ == '__main__':

    setDebug(False)
    import unittest

    hack()

    class UnitTestBaseStrip(unittest.TestCase):

        test_pins = 18, 21, 23

        def setUp(self):
            _ = [setupOutPin(pin) for pin in self.test_pins]
            for pin in self.test_pins:
                self.assertIn(pin, OUT_PINS, 
                        "Failed to setup outpin {}".format(pin))

        def tearDown(self):
            OUT_PINS.clear()

        def test_OutPinToggle(self):
            '''
                Tests all toggle functions which subsequently test  the
                setOutPinHigh, setOutPinLow and setAllOutPins*  functions
            '''
            test_pins = self.test_pins

            # Test toggleAllOutPins twice, to make sure they toggle on and off
            # and tests setAllOutPinsHigh and setAllOutPinsLow
            for i in range(2):
                prev_values = [OUT_PINS[pin] for pin in test_pins]
                toggleAllOutPins()
                curr_values = [OUT_PINS[pin] for pin in test_pins]
                for i in range(len(test_pins)):
                    self.assertNotEqual(curr_values[i], prev_values[i], 
                            "Failed to toggle all outpins")

            # Test toggleOutPin twcie, to make sure it toggles on and off
            # and tests setOutPinHigh and setOutPinLow
            for i in range(2):
                pin = test_pins[0]
                prev_val = OUT_PINS[pin]
                toggleOutPin(pin)
                self.assertNotEqual(OUT_PINS[pin], prev_val, 
                        "Failed to toggle individual outpin")

        def test_InvalidPins(self):
            invalid_pins = [0, 1, 2]
            for pin in invalid_pins:
                self.assertFalse(checkOutPin(pin))
                self.assertFalse(checkInPin(pin))
                self.assertIsNone(getOutPinState(pin))
                self.assertIsNone(getInput(pin))


            
    unittest.main()

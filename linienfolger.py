"""Test motors"""

import time

from buildhat import Hat, Motor, MotorPair,ColorDistanceSensor, Light 
from buildhat.devices import Device
from buildhat.exc import DeviceError, MotorError
from gpiozero import Button
from signal import pause
import time

GPIO_BUTTON_ROT = 20 #Pin 38
GPIO_BUTTON_BLAU = 21 #Pin 40
H1_RST_GPIO = 4
H1_BOOT_GPIO = 22
H2_RST_GPIO = 5
H2_BOOT_GPIO = 6

hat1: Hat = None
hat2: Hat = None
fahren: MotorPair = None
colorsensor: ColorDistanceSensor = None
#button_blau: Button = None
#button_rot: Button = None

THRESHOLD_DISTANCE = 15
# init build hat

def __init__():
    # Initialisiert GPIO 6 mit internem Pull-Up
 #   button_rot = Button(GPIO_BUTTON_ROT)
 #   button_blau = Button(GPIO_BUTTON_BLAU)
    deregister_all()
    hat1 = Hat(
        device="/dev/ttyAMA0",
        reset_gpio=H1_RST_GPIO,
        boot0_gpio=H1_BOOT_GPIO,
        debug=False,
    )
    hat2 = Hat(
        device="/dev/ttyAMA4",
        reset_gpio=H2_RST_GPIO,
        boot0_gpio=H2_BOOT_GPIO,
        debug=False,
    )
    fahren = MotorPair('A', 'B', hat_instance=hat1._instance)
    colorsensor = ColorDistanceSensor('C', hat_instance=hat1._instance)
    print("Init done")

def run(self):

    while True:
        if colorsensor.get_color() == 'black':
            fahren.start(40, 40)
        else:
            fahren.start(-40, -40)


def main():
    __init__()
    button_rot = Button(GPIO_BUTTON_ROT)
    button_blau = Button(GPIO_BUTTON_BLAU)

    print("Wait on Button blau!")
    while  not button_blau.is_pressed:
        time.sleep(0.2)

    run()      

    print("Wait on Button rot!")
    while  not button_rot.is_pressed:
        time.sleep(0.2)    
    print("THE END!")  


def deregister_all():
    """Remove all HATs from the Device registry and clear port tracking.

    Call this after tests complete to leave the process in a clean state,
    e.g. when multiple test modules are run in the same interpreter session.
    """
    for bhat in list(Device._registry.values()):
        try:
            bhat.shutdown()
        except Exception:
            pass
    Device._registry.clear()
    Device._default_key = None
    Device._used.clear()

if __name__ == '__main__':
  main()

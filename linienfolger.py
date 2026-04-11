"""Test motors"""

import time

from buildhat import Hat, Motor, MotorPair,ColorDistanceSensor, Light 
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

class Robot():
    """Test motors"""

    THRESHOLD_DISTANCE = 15
    # init build hat

    def __init__(self):
        self.hat1 = Hat(
            device="/dev/ttyAMA0",
            reset_gpio=H1_RST_GPIO,
            boot0_gpio=H1_BOOT_GPIO,
            debug=False,
        )
        self.hat2 = Hat(
            device="/dev/ttyAMA4",
            reset_gpio=H2_RST_GPIO,
            boot0_gpio=H2_BOOT_GPIO,
            debug=False,
        )

    def run(self):
        """Test 2 HAT dual motor interval"""
      

        # HAT 1 - Motor , ColorDistanceSensor
        fahren = MotorPair('A', 'B', hat_instance=self.hat1._instance)

        h1s1 = ColorDistanceSensor('B', hat_instance=self.hat1._instance)

        # HAT 2 - Light Motor
        h2l1 = Light('A', hat_instance=self.hat2._instance)
        colorsensor = ColorDistanceSensor('C', hat_instance=self.hat1._instance).get_color()



        while True:
            if colorsensor.get_color() == 'black':
                fahren.start(40, 40)
            else:
                fahren.start(-40, -40)


def main():
    # Initialisiert GPIO 6 mit internem Pull-Up
    button_rot = Button(GPIO_BUTTON_ROT)
    button_blau = Button(GPIO_BUTTON_BLAU)

    print("Wait on Button blau!")
    while  not button_blau.is_pressed:
        time.sleep(0.2)

    if button_rot.is_pressed:
        print("Button rot ist GEDRÜCKT (Pin ist LOW)")
    else:
        print("Button rot ist OFFEN (Pin ist HIGH)")
    Robot().run()      

    print("Wait on Button rot!")
    while  not button_rot.is_pressed:
        time.sleep(0.2)    
    print("THE END!")  

if __name__ == '__main__':
  main()



from buildhat import Motor
from buildhat import MotorPair
import RPi.GPIO as GPIO
import time

BUTTON_ROT = 31 #GPIO6
BUTTON_BLAU = 32 #GPIO12

#inti GPIO pin 12, 6 as input with pull-up resistor
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_ROT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_BLAU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("Wait for button press...Blau")

try:
    while GPIO.input(BUTTON_BLAU) == GPIO.HIGH:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)

    #read GPIO pin 12, 6

    print("int motor A")
    lift = Motor('A')
    print("int motor B")
    zange = Motor('B')
    print("int motor C")
    ml = Motor('C')
    print("int motor D")
    mr = Motor('D')

    #fahren = MotorPair('C', 'D')
    #fahren.set_default_speed(50)
    #fahren.run_for_rotations(2)
    #fahren.run_for_rotations(1, speedl=100, speedr=50)
    print("Running lift for -90 and zange for 90 degrees...")
    lift.run_for_degrees(-90)
    zange.run_for_degrees(90)

    time.sleep(2)
    print("Running motors for 90 degrees...")
    ml.run_for_degrees(90)
    mr.run_for_degrees(90)

    print("Done!")
except KeyboardInterrupt:
    GPIO.cleanup() # Reset pins on exit



from buildhat import Motor
from buildhat import MotorPair
from gpiozero import Button
from signal import pause
import time

GPIO_BUTTON_ROT = 12 #Pin 32
GPIO_BUTTON_BLAU = 6 #Pin 31

# Initialisiert GPIO 6 mit internem Pull-Up
button_rot = Button(GPIO_BUTTON_ROT)
button_blau = Button(GPIO_BUTTON_BLAU)

# Motoren initialisieren
print("int motor pair C+D")
fahren = MotorPair('C', 'D')
fahren.set_default_speed(10)  # Setze die Standardgeschwindigkeit auf 10%

print("Wait for button press...Blau")
try:
    while not button_blau.is_pressed:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)

    print("Running lift for -90 and zange for 90 degrees...")
    fahren.run_for_rotations(1)

    print("Stop on Button red...")
    while not button_rot.is_pressed:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)
    
    fahren.stop()
      


    print("Done!")
except KeyboardInterrupt:
    print("Interrupted by user, stopping motors...")
    fahren.stop()
    #fahren.stop()

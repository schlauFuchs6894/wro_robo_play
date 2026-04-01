

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

print("press blue...Run rotations 1")
try:
    while not button_blau.is_pressed:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)

    fahren.run_for_rotations(1) # right turn

    print("press blue... Run rotations 1 10,-10...") #-> fwd left, bwd right
    while not button_blau.is_pressed:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)
    fahren.run_for_rotations(1, speedl=10, speedr=-10)

    print("Wait for button press...Blau")
    while not button_blau.is_pressed:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)

    print("Run rotations 10 10,-10...") #-> fwd left, bwd right
    fahren.run_for_rotations(10, speedl=10, speedr=-10)

    print("Wait for button press...Blau")
    while not button_blau.is_pressed:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)

    print("Run degrees 90 -90...") #-> fwd left, bwd right
    fahren.run_for_degrees(90, speedl=10, speedr=-10)


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

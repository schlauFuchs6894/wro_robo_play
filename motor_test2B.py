

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
print("int motor A")
lift = Motor('A')
print("int motor B")
zange = Motor('B')
print("int motor pair C+D")
fahren = MotorPair('C', 'D')


if button_blau.is_pressed:
    print("Schalter ist GEDRÜCKT (Pin ist LOW)")
else:
    print("Schalter ist OFFEN (Pin ist HIGH)")

# Um den exakten Digitalwert (0 oder 1) zu sehen:
print(f"Digitaler Wert: {button_blau.value}") 
# Hinweis: .value ist bei Button invertiert (1 = gedrückt)


print("Wait for button press...Blau")
try:
    while not button_blau.is_pressed:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)

    #read GPIO pin 12, 6

 
    #fahren.set_default_speed(50)
    #fahren.run_for_rotations(2)
    #fahren.run_for_rotations(1, speedl=100, speedr=50)
    print("Running lift for -90 and zange for 90 degrees...")
    lift.run_for_degrees(-90)
    zange.run_for_degrees(90)

    time.sleep(2)
    print("Running motors for 90 degrees...")
    #ml.run_for_degrees(90)
    #mr.run_for_degrees(90)
    fahren.set_default_speed(20)
    fahren.run_for_rotations(1, speedl=-100, speedr=100)
    fahren.run_to_position(20, 100, speed=20)
    fahren.start(speedl=-30, speedr=30)

    print("Stop on Button red...")
    while not button_rot.is_pressed:
        # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        time.sleep(0.1)
    
    fahren.stop()
      


    print("Done!")
except KeyboardInterrupt:
    print("Interrupted by user, stopping motors...")
    lift.stop()
    zange.stop()
    fahren.stop()
    #fahren.stop()

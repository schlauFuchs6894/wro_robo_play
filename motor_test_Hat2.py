
from buildhat import Motor
from buildhat import MotorPair
from buildhat import Hat, ColorDistanceSensor, Motor
from gpiozero import Button
from signal import pause
import time

GPIO_BUTTON_ROT = 12 #Pin 32
GPIO_BUTTON_BLAU = 6 #Pin 31

# Initialisiert GPIO 6 mit internem Pull-Up
button_rot = Button(GPIO_BUTTON_ROT)
button_blau = Button(GPIO_BUTTON_BLAU)


def run_hat2():
    print(f"[HAT2] process started, PID={os.getpid()}", flush=True)
    try:
        Hat(
            device="/dev/ttyAMA4",
            reset_gpio=25,
            boot0_gpio=24,
            debug=True,
        )
        print(f"[HAT2] init SensorS and Actors")

    except Exception as exc:
        print(
            {
                "hat": 2,
                "event": "error",
                "message": f"init failed: {type(exc).__name__}: {exc}",
            }
        )
        return

    # Motoren initialisieren
    print("int motor A")
    lift = Motor('A')
 

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
      

        print("Done!")
    except KeyboardInterrupt:
        print("Interrupted by user, stopping motors...")
        lift.stop()

if __name__ == "__main__":
   run_hat2()
   
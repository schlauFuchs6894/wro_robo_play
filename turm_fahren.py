"""Test motors"""

import time
from turtle import color

from buildhat import Hat, Motor, MotorPair,ColorDistanceSensor,ColorSensor, Light, DistanceSensor
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
lift: Motor = None
gabel: Motor = None
distance: DistanceSensor = None
color_obj_sensor: ColorSensor = None
color_sensor: ColorDistanceSensor = None
button_blau: Button = None
button_rot: Button = None
object_color: int = None

THRESHOLD_DISTANCE = 100
DEFAULT_DIST = 10
ROTATIONS_PER_CM = 0.1
# init build hat

def setup():
    global button_rot, button_blau, hat1, hat2, lift, gabel,fahren, color_obj_sensor, color_sensor, distance
    # Initialisiert GPIO 6 mit internem Pull-Up
    button_rot = Button(GPIO_BUTTON_ROT)
    button_blau = Button(GPIO_BUTTON_BLAU)
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
    color_sensor = ColorSensor('C', hat_instance=hat1._instance)
    distance = DistanceSensor('D', hat_instance=hat1._instance)
    lift = Motor('A', hat_instance=hat2._instance)
    gabel = Motor('B', hat_instance=hat2._instance)
    color_obj_sensor = ColorDistanceSensor('C', hat_instance=hat2._instance)
    print("Init done")


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

def ready_wait_for_start():
    print("Wait on Button blau!")
    while  not button_blau.is_pressed:
        time.sleep(0.2)    



def ruekwaerts(distance=DEFAULT_DIST):
    rotations = distance * ROTATIONS_PER_CM
    fahren.run_for_rotations(rotations, 40, -40)
    fahren.stop()

def aufluepfen():
    lift.run_for_rotations(1, 50)                                        
    gabel.run_for_degrees(180, 50)


def linenfolger(distanceuntilstop=THRESHOLD_DISTANCE):
    while distance.get_distance() > distanceuntilstop:
       linenfolger_update()
    fahren.stop()

def linenfolger_update():
        if color_sensor.get_color() == 'black':
            print("rechts")
            fahren.start(30, -10)
        else:
            print("links")
            fahren.start(10, -30)


def run():
    global object_color

    while not color_sensor.get_color() == 'white':
        print(color_sensor.get_color())
        fahren.start(30, -30)
    print("c", color_sensor.get_color())
    fahren.stop()
    fahren.run_for_rotations(1, 30, 30)
    fahren.run_for_rotations(3, 30, -30)
    fahren.run_for_rotations(1, -30, -30)
    fahren.run_for_rotations(3, 30, -30)


def main():
    setup()
    ready_wait_for_start()
    run()      

    print("Wait on Button rot!")
    while not button_rot.is_pressed:
        time.sleep(0.2)
    print("THE END!")

if __name__ == '__main__':
  main()

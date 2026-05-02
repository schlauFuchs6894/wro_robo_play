"""Test motors"""
import time
from robo_init import robo, setup, create_motor_pair, ready_wait_for_start, stop_all
# from buildhat import Hat, Motor, MotorPair,ColorDistanceSensor,ColorSensor, Light, DistanceSensor
# from buildhat.devices import Device
# from buildhat.exc import DeviceError, MotorError
from turtle import color
from gpiozero import Button
from signal import pause
import time

THRESHOLD_DISTANCE = 100
DEFAULT_DIST = 10
ROTATIONS_PER_CM = 1.0 / 17.0


def ruekwaerts(distance=DEFAULT_DIST):
    rotations = distance * ROTATIONS_PER_CM
    robo.fahren.run_for_rotations(rotations, 40, -40)
    robo.fahren.stop()

def aufluepfen():
    robo.lift.run_for_rotations(2, 30)                                       
    robo.gabel.run_for_degrees(180, 50)
    robo.lift.run_for_rotations(-2, 30)


def linenfolger(distanceuntilstop=THRESHOLD_DISTANCE):
    while distance.get_distance() > distanceuntilstop:
       linenfolger_update()
    robo.fahren.stop()

def linenfolger_update():
        if robo.color_sensor.get_color() == 'black':
            print("rechts")
            robo.fahren.start(30, -10)
        else:
            print("links")
            robo.fahren.start(10, -30)


def run():
    robo.fahren.stop()
    time.sleep(4)
    gerade1 = ROTATIONS_PER_CM * 22  
    robo.fahren.run_for_rotations(gerade1,20,-20)
    NUNZIG_GRAD = 0.65
    gerade2 = ROTATIONS_PER_CM * 11
    
    # 90° nach links
 
    robo.fahren.run_for_rotations(NUNZIG_GRAD, 40, 40)
    
    robo.fahren.run_for_rotations(gerade2,20,-20)
    
    robo.fahren.run_for_rotations(0.67, -40, -40)
    
    robo.fahren.run_for_rotations(ROTATIONS_PER_CM * 13,20,-20)
    aufluepfen()
    robo.fahren.run_for_rotations(NUNZIG_GRAD, -40, -40)
    robo.fahren.run_for_rotations(2, 30, -30)
    robo.fahren.run_for_rotations(NUNZIG_GRAD, -40, -40)

    while not robo.color_sensor.get_color == "black":
        robo.fahren.start(20, -20)
        time.sleep(0.1)
    else:
        robo.fahren.stop()
    robo.fahren.run_for_rotations(NUNZIG_GRAD, 40, 40)
    


def main():
    setup()
    ready_wait_for_start()
    run()      

    print("Wait on Button rot!")
    while not button_rot.is_pressed:
        time.sleep(0.1)
    print("THE END!")

if __name__ == '__main__':
  main()
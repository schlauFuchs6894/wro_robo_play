"""Test motors"""
import time
from robo_init import robo, setup, create_motor_pair, ready_wait_for_start, stop_all
# from buildhat import Hat, Motor, MotorPair,ColorDistanceSensor,ColorSensor, Light, DistanceSensor
# from buildhat.devices import Device
# from buildhat.exc import DeviceError, MotorError
from gpiozero import Button
from signal import pause
import time

THRESHOLD_DISTANCE = 100
DEFAULT_DIST = 10
ROTATIONS_PER_CM = 0.1
# init build hat

def ruekwaerts(distance=DEFAULT_DIST):
    rotations = distance * ROTATIONS_PER_CM
    robo.fahren.run_for_rotations(rotations, 40, -40)
    robo.fahren.stop()

def aufluepfen():
    robo.lift.run_for_rotations(1, 50)                                        
    robo.gabel.run_for_degrees(180, 50)


def linenfolger(distanceuntilstop=THRESHOLD_DISTANCE):
    while robo.distance.get_distance() > distanceuntilstop:
       linenfolger_update()
       print(robo.distance.get_distance())
    robo.fahren.stop()

def linenfolger_update():
        if robo.color_sensor.get_color() == 'black':
            print("rechts")
            robo.fahren.start(30, -10)
        else:
            print("links")
            robo.fahren.start(10, -30)


def run():
    global object_color
    while not robo.button_rot.is_pressed:
       linenfolger_update()
 
    robo.fahren.stop() 
    while robo.button_rot.is_pressed:
        # wait on release
        time.sleep(0.2)
    print("Stop Sensor read with RED!")
    while not button_rot.is_pressed:
       # Update sensor values
       object_color = robo.obj_robo.color_sensor.get_color()
       line_color = robo.color_sensor.get_color()
       distance_value = distance.get_distance()
       print("Color", line_color)
       print("Distance: ", distance_value)
       print("Object color: ", object_color)

def main():
    setup()
    ready_wait_for_start()
    run()      

    print("Wait on Button rot!")
    while  not button_rot.is_pressed:
        time.sleep(0.2)    
    print("THE END!")  

if __name__ == '__main__':
  main()

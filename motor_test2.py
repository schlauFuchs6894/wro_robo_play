from buildhat import Motor
from buildhat import MotorPair
import time
lift = Motor('A')
zange = Motor('B')
fahren = MotorPair('C', 'D')


fahren.set_default_speed(50)
fahren.run_for_rotations(2)
fahren.run_for_rotations(1, speedl=100, speedr=50)
lift.run_for_degrees(-90)
zange.run_for_degrees(90)

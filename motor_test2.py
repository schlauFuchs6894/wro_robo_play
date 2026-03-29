from buildhat import Motor
from buildhat import MotorPair
import time

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

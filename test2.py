from buildhat import Motor
from buildhat import ColorDistanceSensor
from buildhat import MotorPair
stoppen = False
pair = MotorPair('A', 'B')
pair.set_default_speed(50)
c = ColorDistanceSensor('D')

print("start motor")
pair.run_for_rotations(4, speedl=-20, speedr=20)
pair.stop()
#pair.start()

#c = color.wait_until_color(blue)
#pair.stop()
print("wait on blue")
#c.wait_until_color("blue")
#print("stope onblue")

while(stoppen == False):
  pair.run_for_rotations(0.1, speedl=-20, speedr=20)
  color = c.get_color()
  print(color)
  if(color == "white"):
    stoppen = True
    
print("stoped on blue")
pair.stop()
  

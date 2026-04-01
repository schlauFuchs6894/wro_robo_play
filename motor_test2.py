from buildhat import Motor, ColorDistanceSensor, MotorPair
import time


lift = Motor('B')
color = ColorDistanceSensor('A')
raeder = MotorPair('D', 'C')

while True:
    colorfarbe = color.get_color()

    if colorfarbe == 'black':
        raeder.start()  # fährt vorwärts
        print("Schwarz erkannt: fahre vorwärts")
    else:
        raeder.stop()   # stoppt
        print("Nicht schwarz: stoppt")

    time.sleep(0.1)
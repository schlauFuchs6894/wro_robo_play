from buildhat import Motor, ColorDistanceSensor, MotorPair
import time


lift = Motor('B')
color = ColorDistanceSensor('A')
räder = MotorPair('D', 'E')

while True:
    r, g, b, i = color.get_color_rgb()

    if r < 20 and g < 20 and b < 20:
        fahren.start()  # fährt vorwärts
        print("Schwarz erkannt: fahre vorwärts")
    else:
        fahren.stop()   # stoppt
        print("Nicht schwarz: stoppt")

    time.sleep(0.1)
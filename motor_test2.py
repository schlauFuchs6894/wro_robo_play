from buildhat import Motor, ColorDistanceSensor, MotorPair
import time


lift = Motor('B')
color = ColorDistanceSensor('A')
raeder = MotorPair('D', 'C')
startistpassiert = False
raeder.set_default_speed(30)

while not stoppt:
    if color.get_color() == 'blue':
        raeder.stop()  # einmal stoppen
        stoppt = True
        print("Blau erkannt: stoppe")
    time.sleep(0.1) 

raeder.start()
wait(5)
raeder.stop()

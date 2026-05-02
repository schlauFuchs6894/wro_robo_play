import time

from robo_init import robo, setup, ready_wait_for_start, stop_all


loop_count = 0


def run_test_loop():
    global loop_count

    if loop_count == 0:
        print("motorLeft fwd")
        robo.motor_left.start()

    if loop_count == 20:
        robo.motor_left.stop()
        print("motorRight fwd")
        robo.motor_right.start()

    if loop_count == 40:
        robo.motor_right.stop()
        print("Lift down")
        robo.lift.set_default_speed(20)
        robo.lift.start()

    if loop_count == 60:
        print("Lift up")
        robo.lift.start(-20)

    if loop_count == 80:
        robo.lift.stop()
        print("Gabel schliessen")
        robo.gabel.set_default_speed(20)
        robo.gabel.start()

    if loop_count == 90:
        print("Gabel öffnen")
        robo.gabel.start(-20)

    if loop_count == 100:
        robo.gabel.stop()

        boden_color = robo.color_sensor.get_color()
        print(f"Boden Farbe: {boden_color}")

        object_color = robo.obj_color_sensor.get_color()
        print(f"Objekt Farbe: {object_color}")

        object_entfernung = robo.distance.get_distance()
        print(f"Objekt Entfernung: {object_entfernung}")

        object_entfernung2 = robo.obj_color_sensor.get_distance()
        print(f"Objekt Entfernung 2: {object_entfernung2}")
    if loop_count == 120:
        print("Rote Taste Drücken!")
        
    time.sleep(0.1)
    loop_count += 1


if __name__ == "__main__":
    setup()
    ready_wait_for_start()

    while not robo.button_rot.is_pressed:
        run_test_loop()

    print("THE END!")
    stop_all()
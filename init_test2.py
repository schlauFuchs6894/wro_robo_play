import time

from buildhat import (
    Hat,
    Motor,
    MotorPair,
    ColorDistanceSensor,
    ColorSensor,
    Light,
    DistanceSensor,
    ForceSensor,
    PassiveMotor
)
from buildhat.devices import Device
from gpiozero import Button


CLASS_MAP = {
    "Motor": Motor,
    "MotorPair": MotorPair,
    "ColorSensor": ColorSensor,
    "DistanceSensor": DistanceSensor,
    "ColorDistanceSensor": ColorDistanceSensor,
    "Light": Light,
    "ForceSensor": ForceSensor,
    "PassiveMotor": PassiveMotor
}

GPIO_BUTTON_ROT = 20   # Pin 38
GPIO_BUTTON_BLAU = 21  # Pin 40

H1_RST_GPIO = 4
H1_BOOT_GPIO = 22

H2_RST_GPIO = 5
H2_BOOT_GPIO = 6


hats = {}
hatsInfo = {}
sensAct = {}

button_blau: Button | None = None
button_rot: Button | None = None

motorLeft: Motor | None = None
motorRight: Motor | None = None
lift: Motor | None = None
gabel: Motor | None = None

distance: DistanceSensor | None = None
obj_color_sensor: ColorDistanceSensor | None = None
color_sensor: ColorSensor | None = None

loop_count = 0

def setup():
    global button_rot, button_blau
    global hats, hatsInfo, sensAct
    global motorLeft, motorRight, lift, gabel
    global obj_color_sensor, color_sensor, distance

    button_rot = Button(GPIO_BUTTON_ROT)
    button_blau = Button(GPIO_BUTTON_BLAU)

    deregister_all()

    hats, hatsInfo = init_hat()
    sensAct = create_sensAct(hats, hatsInfo)

    motorLeft = sensAct["Hat1"]["motor1"]
    motorRight = sensAct["Hat1"]["motor2"]
    motorRight.reverse() #Reverse polarity

    color_sensor = sensAct["Hat1"]["colorSensor1"]
    distance = sensAct["Hat1"]["distanceSensor1"]

    gabel = sensAct["Hat2"]["motor1"]
    lift = sensAct["Hat2"]["motor2"]

    obj_color_sensor = sensAct["Hat2"]["colorDistanceSensor1"]
    stop_all()
    set_default()

    print("Init done")

def stop_all():
    motorLeft.stop()
    motorRight.stop()
    lift.stop()
    gabel.stop()    

def set_default():
    motorLeft.set_default_speed(20)
    motorRight.set_default_speed(-20)
    lift.set_default_speed(20)
    gabel.set_default_speed(20)   

def init_hat():
    hats_local = {
        "Hat1": Hat(
            device="/dev/ttyAMA0",
            reset_gpio=H1_RST_GPIO,
            boot0_gpio=H1_BOOT_GPIO,
            debug=False,
        ),
        "Hat2": Hat(
            device="/dev/ttyAMA4",
            reset_gpio=H2_RST_GPIO,
            boot0_gpio=H2_BOOT_GPIO,
            debug=False,
        ),
    }

    hats_info_local = {}

    for hat_name, hat in hats_local.items():
        try:
            hats_info_local[hat_name] = hat.get() or {}
        except Exception as e:
            print(f"ERROR: {hat_name} get() failed: {e}")
            hats_info_local[hat_name] = {}

    print_hats_info(hats_info_local)

    return hats_local, hats_info_local


def print_hats_info(hats_info):
    for hat_name, ports in hats_info.items():
        print(f"{hat_name}:")

        for port, data in ports.items():
            print(f"  {port}:")

            for key, value in data.items():
                print(f"    {key}: {value}")


def create_sensAct(hats_local, hats_info_local):
    sens_act = {}

    for hat_name, hat in hats_local.items():
        ports = hats_info_local.get(hat_name, {})
        sens_act[hat_name] = create_devices(ports, hat._instance)

    return sens_act


def to_var_name(name, counter):
    return name[0].lower() + name[1:] + str(counter)


def create_devices(ports, hat_instance):
    devices = {}
    counters = {}

    for port, info in ports.items():
        if not info.get("connected"):
            continue

        cls_name = info.get("name")
        cls = CLASS_MAP.get(cls_name)

        if not cls:
            print(f"WARNING: Unknown class: {cls_name}")
            continue

        counters.setdefault(cls_name, 0)
        counters[cls_name] += 1

        var_name = to_var_name(cls_name, counters[cls_name])

        try:
            devices[var_name] = cls(port, hat_instance=hat_instance)
            print(f"Created {var_name}: {cls_name} on port {port}")
        except Exception as e:
            print(f"ERROR: could not create {var_name} on port {port}: {e}")

    return devices


def deregister_all():
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
        time.sleep(0.1)    



def run_test_loop():
    global loop_count
    if loop_count == 0:
        print("motorLeft fwd")
        motorLeft.start()
    if loop_count == 20:
        motorLeft.stop()
        print("motorRight fwd")
        motorRight.start()
    if loop_count == 40:
        motorRight.stop()
        print("Lift down")
        lift.set_default_speed(20)
        lift.start()
    if loop_count == 60:
        print("Lift up")
        lift.start(-20)
    if loop_count == 80:
        lift.stop()
        print("Gabel schliessen")
        gabel.set_default_speed(20)
        gabel.start()
    if loop_count == 90:
        print("Gabel öffnen")
        gabel.start(-20)
    if loop_count == 100:
        gabel.stop()
        boden_color = color_sensor.get_color()
        print(f"Boden Farbe: {boden_color}")
        object_color = obj_color_sensor.get_color()
        print(f"Objekt Farbe: {object_color}")
        object_entfernung = distance.get_distance()
        print(f"Objekt Entfernung: {object_entfernung}")
        object_entfernung2 = obj_color_sensor.get_distance()
        print(f"Objekt Entfernung 2: {object_entfernung2}")
    if loop_count == 120:
        print("Rote Taste drücken!")

    time.sleep(0.1)
    loop_count += 1

if __name__ == "__main__":
   setup()
   ready_wait_for_start()
   while not button_rot.is_pressed:
     run_test_loop()
     
   print("THE END!")  
   stop_all()
   

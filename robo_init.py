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
    PassiveMotor,
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
    "PassiveMotor": PassiveMotor,
}

GPIO_BUTTON_ROT = 20
GPIO_BUTTON_BLAU = 21

H1_RST_GPIO = 4
H1_BOOT_GPIO = 22

H2_RST_GPIO = 5
H2_BOOT_GPIO = 6


class RoboState:
    def __init__(self):
        self.hats = {}
        self.hats_info = {}
        self.sens_act = {}

        self.button_blau = None
        self.button_rot = None

        self.motor_left = None
        self.motor_right = None
        self.lift = None
        self.gabel = None

        self.distance = None
        self.obj_color_sensor = None
        self.color_sensor = None


robo = RoboState()


def setup():
    deregister_all()

    robo.button_rot = Button(GPIO_BUTTON_ROT)
    robo.button_blau = Button(GPIO_BUTTON_BLAU)

    robo.hats, robo.hats_info = init_hats()
    robo.sens_act = create_sens_act(robo.hats, robo.hats_info)

    robo.motor_left = robo.sens_act["Hat1"]["motor1"]
    robo.motor_right = robo.sens_act["Hat1"]["motor2"]
    robo.motor_right.reverse()

    robo.color_sensor = robo.sens_act["Hat1"]["colorSensor1"]
    robo.distance = robo.sens_act["Hat1"]["distanceSensor1"]

    robo.gabel = robo.sens_act["Hat2"]["motor1"]
    robo.lift = robo.sens_act["Hat2"]["motor2"]

    robo.obj_color_sensor = robo.sens_act["Hat2"]["colorDistanceSensor1"]

    stop_all()
    set_default()

    print("Init done")
    return robo


def init_hats():
    hats = {
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

    hats_info = {}

    for hat_name, hat in hats.items():
        try:
            hats_info[hat_name] = hat.get() or {}
        except Exception as e:
            print(f"ERROR: {hat_name} get() failed: {e}")
            hats_info[hat_name] = {}

    print_hats_info(hats_info)
    return hats, hats_info


def print_hats_info(hats_info):
    for hat_name, ports in hats_info.items():
        print(f"{hat_name}:")

        for port, data in ports.items():
            print(f"  {port}:")

            for key, value in data.items():
                print(f"    {key}: {value}")


def create_sens_act(hats, hats_info):
    sens_act = {}

    for hat_name, hat in hats.items():
        ports = hats_info.get(hat_name, {})
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


def set_default():
    robo.motor_left.set_default_speed(20)
    robo.motor_right.set_default_speed(-20)
    robo.lift.set_default_speed(20)
    robo.gabel.set_default_speed(20)


def stop_all():
    for motor in [
        robo.motor_left,
        robo.motor_right,
        robo.lift,
        robo.gabel,
    ]:
        if motor is not None:
            motor.stop()


def ready_wait_for_start():
    print("Wait on Button blau!")

    while not robo.button_blau.is_pressed:
        time.sleep(0.1)


def deregister_all():
    for bhat in list(Device._registry.values()):
        try:
            bhat.shutdown()
        except Exception:
            pass

    Device._registry.clear()
    Device._default_key = None
    Device._used.clear()
# pip install pytest
# pytest -v  - run test

import sys
import types
import importlib


class FakeDeviceBase:
    _registry = {}
    _default_key = None
    _used = set()


class FakeHat:
    def __init__(self, *args, **kwargs):
        self._instance = object()
        self.device = kwargs.get("device")

    def get(self):
        if self.device == "/dev/ttyAMA4":
            return {
                "A": {"name": "Motor", "connected": True},
                "B": {"name": "Motor", "connected": True},
                "C": {"name": "ColorDistanceSensor", "connected": True},
            }

        return {
            "A": {"name": "Motor", "connected": True},
            "B": {"name": "Motor", "connected": True},
            "C": {"name": "ColorSensor", "connected": True},
            "D": {"name": "DistanceSensor", "connected": True},
        }


class FakeMotor:
    def __init__(self, port, hat_instance=None):
        self.port = port
        self.hat_instance = hat_instance
        self.speed = None
        self.stopped = False
        self.reversed = False

    def stop(self):
        self.stopped = True

    def start(self, speed=None):
        self.speed = speed

    def set_default_speed(self, speed):
        self.speed = speed

    def reverse(self):
        self.reversed = True


class FakeSensor:
    def __init__(self, port, hat_instance=None):
        self.port = port

    def get_color(self):
        return "red"

    def get_distance(self):
        return 123


class FakeButton:
    def __init__(self, pin):
        self.pin = pin
        self.is_pressed = True


def install_fake_modules(monkeypatch):
    fake_buildhat = types.ModuleType("buildhat")
    fake_buildhat.Hat = FakeHat
    fake_buildhat.Motor = FakeMotor
    fake_buildhat.MotorPair = FakeMotor
    fake_buildhat.ColorDistanceSensor = FakeSensor
    fake_buildhat.ColorSensor = FakeSensor
    fake_buildhat.Light = FakeSensor
    fake_buildhat.DistanceSensor = FakeSensor
    fake_buildhat.ForceSensor = FakeSensor
    fake_buildhat.PassiveMotor = FakeMotor

    fake_devices = types.ModuleType("buildhat.devices")
    fake_devices.Device = FakeDeviceBase

    fake_gpiozero = types.ModuleType("gpiozero")
    fake_gpiozero.Button = FakeButton

    monkeypatch.setitem(sys.modules, "buildhat", fake_buildhat)
    monkeypatch.setitem(sys.modules, "buildhat.devices", fake_devices)
    monkeypatch.setitem(sys.modules, "gpiozero", fake_gpiozero)


def load_robo_init(monkeypatch):
    install_fake_modules(monkeypatch)

    if "robo_init" in sys.modules:
        del sys.modules["robo_init"]

    return importlib.import_module("robo_init")


def test_to_var_name(monkeypatch):
    robo_init = load_robo_init(monkeypatch)

    assert robo_init.to_var_name("Motor", 1) == "motor1"
    assert robo_init.to_var_name("ColorSensor", 2) == "colorSensor2"


def test_create_devices(monkeypatch):
    robo_init = load_robo_init(monkeypatch)

    ports = {
        "A": {"name": "Motor", "connected": True},
        "B": {"name": "Motor", "connected": True},
        "C": {"name": "ColorSensor", "connected": True},
        "D": {"name": "UnknownDevice", "connected": True},
        "E": {"name": "Motor", "connected": False},
    }

    devices = robo_init.create_devices(ports, hat_instance=object())

    assert "motor1" in devices
    assert "motor2" in devices
    assert "colorSensor1" in devices
    assert "unknownDevice1" not in devices
    assert "motor3" not in devices


def test_setup(monkeypatch):
    robo_init = load_robo_init(monkeypatch)

    robo = robo_init.setup()

    assert robo.motor_left is not None
    assert robo.motor_right is not None
    assert robo.color_sensor is not None
    assert robo.distance is not None

    assert robo.motor_right.reversed is True
    assert robo.motor_left.speed == 20
    assert robo.motor_right.speed == -20
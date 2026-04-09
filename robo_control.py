#!/usr/bin/env python3

import time

from multiprocessing import Process, Queue, set_start_method
from queue import Empty
from gpiozero import Button
from signal import pause
from hat1_process import run_hat1
from hat2_process import run_hat2

GPIO_BUTTON_ROT = 20 #Pin 38
GPIO_BUTTON_BLAU = 21 #Pin 40

# Initialisiert GPIO 6 mit internem Pull-Up
#button_rot = Button(GPIO_BUTTON_ROT)
#button_blau = Button(GPIO_BUTTON_BLAU)

class Robot:
    TICK_TIME = 1.0
    TICK_MODULO = 10

    def __init__(self):
        self.hat1_cmd_q = Queue()
        self.hat1_evt_q = Queue()
        self.hat2_cmd_q = Queue()
        self.hat2_evt_q = Queue()
        self._p1: Process = None
        self._p2: Process = None

        self.speed = 0.0
        self.turn = 0.0
        self.lift = 0.0
        self.zange = 0.0
        self.deadline = time.time() 
        self._tick: int = 0

    def setTimeout(self, duration):
        self.deadline = time.time() + duration
    
    def timeExpired(self):
        return (time.time() >= self.deadline)

    def start(self, hat_timeout: float = 20.0):
        """Start both HAT worker processes and wait until ready."""
        set_start_method("spawn", force=True)

        self._p2 = Process(target=run_hat2, args=(self.hat2_cmd_q, self.hat2_evt_q), daemon=True)
        self._p2.start()

        time.sleep(5.0)

        self._p1 = Process(target=run_hat1, args=(self.hat1_cmd_q, self.hat1_evt_q), daemon=True)
        self._p1.start()

        time.sleep(1.0)
        self.wait_for_event(self.hat2_evt_q, 2, "ready", timeout=hat_timeout)
        print("HAT 2 ready.")
        self.wait_for_event(self.hat1_evt_q, 1, "ready", timeout=hat_timeout)
        print("HAT 1 ready.")

    def stop(self):
        """Shutdown both HAT worker processes."""
        self.hat1_cmd_q.put({"action": "shutdown"})
        self.hat2_cmd_q.put({"action": "shutdown"})

        try:
            self.wait_for_event(self.hat1_evt_q, 1, "stopped", timeout=5.0)
        except Exception:
            pass
        try:
            self.wait_for_event(self.hat2_evt_q, 2, "stopped", timeout=5.0)
        except Exception:
            pass

        if self._p1:
            self._p1.join(timeout=2.0)
        if self._p2:
            self._p2.join(timeout=2.0)

    def wait_for_event(self, evt_q: Queue, hat_id: int, expected: str, timeout: float = 10.0) -> dict:
        """Block until a specific event arrives from a HAT worker.

        :param evt_q: Event queue to listen on
        :param hat_id: HAT id to filter for
        :param expected: Event name to wait for
        :param timeout: Seconds before TimeoutError is raised
        :return: The matching event dict
        :raises RuntimeError: If an error event is received
        :raises TimeoutError: If timeout expires before event arrives
        """
        deadline = time.time() + timeout
        buffer = []

        while time.time() < deadline:
            remaining = max(0.0, deadline - time.time())
            try:
                evt = evt_q.get(timeout=min(0.2, remaining))
            except Empty:
                continue

            if evt.get("hat_id") == hat_id and evt.get("event") == "error":
                for item in buffer:
                    evt_q.put(item)
                raise RuntimeError(f"HAT {hat_id} error: {evt.get('message')}")

            if evt.get("hat_id") == hat_id and evt.get("event") == expected:
                for item in buffer:
                    evt_q.put(item)
                return evt

            buffer.append(evt)

        for item in buffer:
            evt_q.put(item)

        raise TimeoutError(f"Timeout waiting for HAT {hat_id} event '{expected}'")

    def drain_events(self, evt_q: Queue, duration: float = 1.0):
        """Drain and print all events from a queue for a given duration."""
        deadline = time.time() + duration
        while time.time() < deadline:
            try:
                evt = evt_q.get(timeout=0.1)
            except Empty:
                continue
            print(f"EVENT: {evt}")

    # ------------------------------------------------------------------
    # HAT 1 commands
    # ------------------------------------------------------------------
    def hat1_motor_start(self, speed: int = 30):
        self.hat1_cmd_q.put({"action": "motor_start", "speed": speed})
        return self.wait_for_event(self.hat1_evt_q, 1, "motor_started")

    def hat1_motor_stop(self):
        self.hat1_cmd_q.put({"action": "motor_stop"})
        return self.wait_for_event(self.hat1_evt_q, 1, "motor_stopped")

    def hat1_read_distance(self):
        self.hat1_cmd_q.put({"action": "read_distance"})
        evt = self.wait_for_event(self.hat1_evt_q, 1, "distance")
        return evt.get("value")

    # ------------------------------------------------------------------
    # HAT 2 commands
    # ------------------------------------------------------------------
    def hat2_motor_start(self, speed: int = 30):
        self.hat2_cmd_q.put({"action": "motor_start", "speed": speed})
        return self.wait_for_event(self.hat2_evt_q, 2, "motor_started")

    def hat2_motor_stop(self):
        self.hat2_cmd_q.put({"action": "motor_stop"})
        return self.wait_for_event(self.hat2_evt_q, 2, "motor_stopped")

    def hat2_read_distance(self):
        self.hat2_cmd_q.put({"action": "read_distance"})
        evt = self.wait_for_event(self.hat2_evt_q, 2, "distance")
        return evt.get("value")
    
    def loop(self):
        if self.timeExpired():
            self.setTimeout(1)
            dist = self.hat1_read_distance()
            print(dist)
            ++self._tick

        if self._tick % self.TICK_MODULO == 0:   
            self.hat1_motor_stop()
            

        # # 1) Read distance from Hat 1 Sensor D
        # hat1_cmd_q.put({"action": "read_distance"})
        # evt1 = wait_for_event(hat1_evt_q, 1, "distance", timeout=5.0)
        # print(f"Hat 1 Sensor D distance: {evt1['value']}")

        # # 2) Read distance from Hat 2 Sensor D
        # hat2_cmd_q.put({"action": "read_distance"})
        # evt2 = wait_for_event(hat2_evt_q, 2, "distance", timeout=5.0)
        # print(f"Hat 2 Sensor D distance: {evt2['value']}")

        # # 3) Run Motor 1 on Hat 1 Motor A
        # hat1_cmd_q.put({"action": "motor_start", "speed": 30})
        # wait_for_event(hat1_evt_q, 1, "motor_started", timeout=5.0)
        # print("Hat 1 Motor A started.")

        # # 4) Run Motor 2 on Hat 2 Motor A
        # hat2_cmd_q.put({"action": "motor_start", "speed": 30})
        # wait_for_event(hat2_evt_q, 2, "motor_started", timeout=5.0)
        # print("Hat 2 Motor A started.")

        # time.sleep(3.0)

        # # Stop both motors again
        # hat1_cmd_q.put({"action": "motor_stop"})
        # hat2_cmd_q.put({"action": "motor_stop"})
        # wait_for_event(hat1_evt_q, 1, "motor_stopped", timeout=5.0)
        # wait_for_event(hat2_evt_q, 2, "motor_stopped", timeout=5.0)


def main():

    robot = Robot()
    robot.start()

    try:
        
        # if button_blau.is_pressed:
        #     print("Schalter ist GEDRÜCKT (Pin ist LOW)")
        # else:
        #     print("Schalter ist OFFEN (Pin ist HIGH)")

        print("Wait for button press...Blau")

        # while not button_blau.is_pressed:
        #     # In pull-up mode, the pin is 0 (LOW) when the switch is pressed
        #     time.sleep(0.1)
        #     drain_events(hat1_evt_q, duration=1.0)
        #     drain_events(hat2_evt_q, duration=1.0)
        
        robot.hat1_motor_start()

        while(True):
            # if button_rot.is_pressed:
            #     print("Schalter ROT ist GEDRÜCKT (Pin ist LOW)")
            #     break;
            robot.loop()
 
    finally:
        print("Finally STOP")
        robot.stop()


if __name__ == "__main__":
    main()
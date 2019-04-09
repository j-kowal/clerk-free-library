"""
Author: Jan Kowal

Description:

Class controlling servo motors in the system
"""

from gpiozero import Servo as _s
from time import sleep
from RPi import GPIO

class Servo:

    def __init__(self):
        # dictionary with GPIO ports
        self._dict = {
            1: 17,
            2: 27
        }

    # move required servo motor
    def move(self, motor_no):
        s = _s(self._dict[motor_no])
        while True:
            s.max()
            sleep(1)
            s.min()
            sleep(1)
            break
        GPIO.cleanup(motor_no) # clean up resources for another sensors
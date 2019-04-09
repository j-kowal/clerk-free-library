"""
Author: Jan Kowal

Description:

Class controlling the LED light - dedicated for RFID reader
"""

from gpiozero import LED as L

class LED:

    _led_port = 21 # led light GPIO port

    def __init__(self):
        self._led = L(self._led_port)
        self._led.off()

    # switch on
    def on(self):
        self._led.on()

    # switch off
    def off(self):
        self._led.off()
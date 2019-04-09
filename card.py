"""
Author: Jan Kowal

Description:

This class handling all the RFID reader operations. It's inheriting Thread class and running as a separate thread.
"""

from time import sleep
import RPi.GPIO as GPIO
# SimpleMFRC522 Code by Simon Monk https://github.com/simonmonk/
from mfrc522 import SimpleMFRC522
from led import LED
from firebase import Firebase
from threading import Thread

class Scan(Thread):

    # private properties
    _fb = Firebase()
    _l = LED()

    # is_working indicator
    is_working = True

    # constructor
    def __init__(self):
        # calling constructor from parent class Thread
        Thread.__init__(self)

    # scan method - scans rfid tag
    def scan(self):
        try:
            # read the uid of the tag
            reader = SimpleMFRC522()
            id_no, text = reader.read()
            # if id exists
            if id_no is not None and isinstance(id_no, int):
                # call return the book method from firebase class
                self._fb.return_the_book(str(id_no))
                #turn the LED for 2 seconds
                self._l.on()
                sleep(2)
                self._l.off()

        except():
            # if fail clean GPIO
            GPIO.cleanup()
            raise

    # run method - called on Thread.start()
    def run(self):
        while True:
            if self.is_working:
                self.scan()
            else:
                # if is not working clean the GPIO for servo motors
                GPIO.cleanup()
                return
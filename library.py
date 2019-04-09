"""
Author: Jan Kowal

Description:

Main application class
"""

from firebase import Firebase
from time import sleep
from facial_recognition import FacialRecognition
from servo import Servo
from threading import Thread
from card import Scan
from pynput.keyboard import Key, Listener
import keyboard
from console import Console

# objects
fb = Firebase()
fr = FacialRecognition()
s = Servo()

# a keypress listener looking for even when 'r' key is pressed
def on_press(key):
    if keyboard.is_pressed('r'):
        fr.is_registration_on = True

# listening thread
def listen():
    while True:
        # getting all JSON data from the firebase
        data = fb.get_data()

        # checking if there is new 'rent a book' request
        if data['vending']['is_processing'] is True:
            # switch off the scan
            scan_t.is_working = False
            # process request from firebase
            key = str(data['vending']['requested_id'])
            # move the servo to release the book
            s.move(int(data['books'][key]['servo']))
            user = str(data['vending']['user_id'])
            date = str(data['vending']['rented_date'])
            # update the processed
            fb.update_data({
                "vending/is_processing" : False,
                "books/%s/rented_by" % key : user,
                "books/%s/rented_date" % key : date,
                "books/%s/servo" % key: "0"
            })
            # put the RFID scanner back to work
            scan_t.is_working = True

        # thread hold for 1s
        sleep(1)

# local helper - will schedule registration process in FacialRecognition class -> def take_pictures
def take_pictures():
    fb.update_data({
        "registration_on_progress": True
    })
    # triggers registration process
    fr.take_pictures()

# updating thread
def update():
    while True:
        # checking possible scenarios with registration
        # 1. if registration was requested and faces trainer yml file exists
        if fr.is_registration_on is True and fr.trainer_exists() is False:
            take_pictures()
            fr.load_trainer()
        # 2. if registration was requested and faces trainer yml file exists
        elif fr.is_registration_on is True and fr.trainer_exists():
            take_pictures()
        # 3. else just keep screening for faces
        else:
            fr.recognize()

# main method
if __name__ == '__main__':
    # creating three threads 1 - listening, 2 - updating, 3 - reading RFID tags, 4 - listening for keyboard input
    listen_t = Thread(target=listen)
    update_t = Thread(target=update)
    scan_t = Scan()
    keyboard_t = Listener(on_press=on_press)
    Console.clear()
    Console.show_reg_msg()

    # running threads simultaneously
    listen_t.start()
    update_t.start()
    scan_t.start()
    keyboard_t.start()

    # join threads to the main thread
    listen_t.join()
    update_t.join()
    scan_t.join()
    keyboard_t.join()

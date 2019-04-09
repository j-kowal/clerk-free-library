"""
Author: Jan Kowal

Description:

This class is handling all facial recognition related operations
"""

import cv2
import os
import numpy as np
from PIL import Image
from time import sleep
from servo import Servo
from firebase import Firebase
import random
import getpass
from termios import tcflush, TCIOFLUSH
from sys import stdin, stdout
from console import Console


class FacialRecognition:

    # constant private variables
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    _images_dir = os.path.join(_BASE_DIR, "user")
    _fb = Firebase()

    # indicator if registration is going on
    is_registration_on = False

    # bool value returned in relation to check if trained faces file exists.
    @staticmethod
    def trainer_exists():

        return os.path.exists('trainer.yml')

    # loads .yml file of trainer
    def load_trainer(self):

        self._face_detector.read('trainer.yml')

    # constructor class
    def __init__(self):

        self._video = cv2.VideoCapture(0) # capture video from source '0' - raspi camera
        # load face detection instructions - Created by Rainer Lienhart.
        self._cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
        self._face_detector = cv2.face.LBPHFaceRecognizer_create() # creates face recognizer
        if self.trainer_exists(): # checks if trainer.yml exists
            self.load_trainer()
        self._servo = Servo()
        self._fb = Firebase()

    # convert's picture to grey using open cv method
    @staticmethod
    def _convert_to_grey(picture):

        return cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)

    # method which is looping recognising face front of the camera.
    def recognize(self):

        # ret - return boolean and frame is the current frame captured from the camera
        ret, frame = self._video.read()
        gray = self._convert_to_grey(frame)
        # detect faces through the cascade instructions
        faces = self._cascade.detectMultiScale(gray, 1.3, 5)

        # iterating through found objects
        for (x, y, w, h) in faces:
            # if user_id was associated with the face set active user
            face_id, score = self._face_detector.predict(gray[y: y + h, x: x + w])
            self._fb.set_active_user(face_id)

    # train faces method
    def train_faces(self):

        faces = [] # an empty array for faces numeric arrays
        ids = [] # an empty array for user's id

        # walk through images in /user folder
        for root, dirs, images in os.walk(self._images_dir):
            for img in images:
                # if img has .jpg extension
                if img.endswith("jpg"):

                    face_id = int(os.path.basename(root)) # getting face_id out of the folder name
                    path = os.path.join(root, img) # getting the path out of the picture number and root folder
                    grey_img = Image.open(path).convert('L') # converts image to gray
                    img_arr = np.array(grey_img, 'uint8') # creating numpy array out of the picture

                    # takes currently loaded image and detects face on it.
                    temp = self._cascade.detectMultiScale(img_arr)
                    for (x, y, w, h) in temp:
                        faces.append(img_arr[y:y + h, x:x + w]) # append face's array to faces array
                        ids.append(face_id) # appends id to an ids array

                    self._face_detector.train(faces, np.array(ids)) # run's and train algorithm with detector instructions
                    self._face_detector.save('trainer.yml') # saves yml output

    # the user registration process
    def take_pictures(self):
        Console.clear()
        print('Preparing ...')
        sleep(2)
        # flushes input buffer to prevent user input concatenation with previously pressed keys
        stdout.flush()
        tcflush(stdin, TCIOFLUSH)
        Console.clear()

        # Q1
        email = input("What's email address?\n")

        # password loop to make sure user is entering the correct one.
        while True:
            password1 = getpass.getpass("Set up your password (min 6 chars).\n")
            password2 = getpass.getpass("Repeat your password.\n")
            if password1 == password2:
                break

        # create firebase credentials
        self._fb.create_user(email, password1)

        # time countdown before take the picture (5s)
        ct = 5
        Console.clear()
        while ct > 0:
            print('Please look at the camera now. We will take a few pictures in: %s' % ct)
            sleep(1)
            ct = ct - 1
            os.system('clear')

        # check if folder already exists
        if os.path.exists('user') is False:
            os.mkdir('user')

        # get random id and if exists re-randomize again
        user_id = random.SystemRandom().randint(10000,99999)
        while True:
            if os.path.exists('user/%s' % user_id) is False:
                os.mkdir('user/%s' % user_id)
                self._fb.update_data({
                    "users/%s" % user_id : email
                })
                break
            else:
                user_id = random.SystemRandom().randint(10000,99999)

        counter = 0 # will count pictures which were taken

        # taking user's pictures
        while True:
            ret, frame = self._video.read() # ret - bool, frame - current camera frame
            gray = self._convert_to_grey(frame) # convert picture to greyscale
            faces = self._cascade.detectMultiScale(gray, 1.3, 5) # detect faces

            # iterate through detected
            for (x, y, w, h) in faces:
                cv2.imwrite("user/%s/%s.jpg" % (user_id, counter), gray[y: y + h, x: x + w])

                counter = counter + 1
            if counter == 10: # at the 10th picture stop
                self.train_faces() # run train algorithm

                # print successful message
                Console.clear()
                print('Your profile was created! Thanks!')
                sleep(3)

                # update broker and system with the information on registration
                self._fb.update_data({
                    "registration_on_progress": False
                })
                self.is_registration_on = False
                # show a regular message on the display
                Console.show_reg_msg()
                break

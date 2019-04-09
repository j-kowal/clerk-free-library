"""
Author: Jan Kowal

Description:

Firebase class that has all functionality to upload and download data from the broker
"""

# imports
import pyrebase
from datetime import datetime

class Firebase:

    #Firebase DB config
    _config = {
        "apiKey": "<apiKey>",
        "authDomain": "<authDomain>",
        "databaseURL": "<databaseURL>",
        "projectId": "<projectId>",
        "storageBucket": "<storageBucket>",
        "messagingSenderId": "<messagingSenderId>",
        "serviceAccount": "<path_to_file>"
    }

    # login credentials as private access vars
    _login = "<login>"
    _password = "<password>"

    # update data method
    def update_data(self, data):
        self._db.update(data)

    # action for returning the book by the user
    def return_the_book(self, id):
        self._db.update({
            "books/%s/rented_by" % id: "",
            "books/%s/rented_date" % id: "",
        })

    # get data method
    def get_data(self):
        return self._db.get().val()

    # set active user - one front of the camera
    def set_active_user(self, face_id):
        email = self.get_data()['users'][str(face_id)]
        self.update_data({
            "login/current_email" : email,
            "login/last_seen" : datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

    # create user with the firebase credentials
    def create_user(self, email, password):
        self._auth.create_user_with_email_and_password(email, password)

    #Constructor method
    def __init__(self):
        # initialize firebase instance
        self._firebase = pyrebase.initialize_app(self._config)
        self._auth = self._firebase.auth()
        self._user = self._auth.sign_in_with_email_and_password(self._login, self._password)
        self._db = self._firebase.database()
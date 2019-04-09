# Clerk Free Library

<img src="https://i.imgur.com/3SntxT9.jpg" width="300" height="380">


Clerk Free Library is an IoT prototype system that allows the user to rent books without librarian intervention. Originally built out of the shoebox with two servo motors to vend books. The system is using Open CV 4 library for facial recognition, RFID scanner, Raspberry Pi 3 B+ and Firebase as a message broker. It can easily react with other devices using Firebase.

# Python Dependencies

* [Pyrebase](https://github.com/thisbejim/Pyrebase) - Connection with Firebase.
* [Open CV 4](https://opencv.org/) - Facial Recognition Library.
* [MFRC522-python](https://github.com/pimylifeup/MFRC522-python) - RFID reader library.
* [gpiozero](https://gpiozero.readthedocs.io/) - For servos.

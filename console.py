"""
Author: Jan Kowal

Description:

This class handling all the Console output for registering user.

"""

from os import system

class Console:

    # display regular text
    @staticmethod
    def show_reg_msg():
        print('CLERK-FREE LIBRARY v1\n\nif you would like to register please press the R key')

    # clear the console
    @staticmethod
    def clear():
        system('clear')
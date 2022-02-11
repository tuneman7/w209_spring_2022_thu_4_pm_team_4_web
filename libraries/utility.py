import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp


class Utility:
    '''
    Utility class to handle things that all of the other classes may need.  File / screen access etc.
    '''

    screen_width = 76
    def __init__(self):
        self.bozo ="bozo"
        self.screen_width = 76

    # define our clear function
    def clear(self):
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')


    def get_data_from_file(self,str_file_name,current_dir=False):
        '''
        Read an entire file and push the data back.
        :param str_file_name:
        :return:
        '''
        if current_dir==True:
            str_file_name = os.path.join(self.get_this_dir(),str_file_name)
        with open(str_file_name, 'r') as file:
            data = file.read()

        return data

    def get_this_dir(self):
        '''
        Return the working directory.
        :return:
        '''
        thisdir = os.getcwd()
        return thisdir


import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandasql as psql


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


    def get_data_from_file(self,str_file_name):
        '''
        Read an entire file and push the data back.
        :param str_file_name:
        :return:
        '''
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


class import_export_data(Utility):
    
    ALL_COUNTRIES_DATA_FRAME = None


    def __init__(self,**kwargs):
        allowed_keys = {'zipcode', 'search_uri', 'description'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def __init__(self):
        super().__init__()
        global ALL_COUNTRIES_DATA_FRAME
        ALL_COUNTRIES_DATA_FRAME = self.load_and_clean_up_top_20_file()


    def print_internal_directory(self):

        for k,v in self.__dict__.items():
            print("{} is \"{}\"".format(k,v))

    def get_top_20_full_file_name(self) :

        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        top_20_file_name = "top20_2014-2020_all.csv"

        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,top_20_file_name)

        return return_file_name

    def load_and_clean_up_top_20_file(self):

        file_to_load = self.get_top_20_full_file_name()

        my_data = pd.read_csv(file_to_load)
        
        return my_data

    def get_sql_for_world_or_region(self, source_country):
        my_sql = '''
        SELECT
            'World' [Trading Partner],
            sum([Total Trade ($M)])  [Total Trade ($M) ],
            avg([RtW (%)])  [RtW (%)],
            sum([Exports ($M)] )[Exports ($M)],
            avg([RtW (%).1])  [RtW (%).1],
            sum([Imports ($M)])  [Imports ($M)],
            avg([RtW (%).2])  [RtW (%).2],
            sum([Net Exports ($M)])  [Net Exports ($M)],
            ''  [Exports Ticker],
            ''  [Imports Ticker],
            country,
            year
        FROM 
            my_data_frame
        WHERE 
            country =  \'''' + source_country + '''\'
        and
            [Trading Partner] <> \'''' + source_country + '''\'
        GROUP BY
            country, year
        '''
        #print(my_sql)
        return my_sql


    def get_data_by_source_and_target_country(self,source_country,target_country):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        if target_country.lower() == "world":
            my_sql = self.get_sql_for_world_or_region(source_country)
        else:
            my_sql = "SELECT * FROM my_data_frame WHERE country = '" +  source_country + "' and [Trading Partner] = '" + target_country + "' "

        my_return_data = psql.sqldf(my_sql)

        return my_return_data


    def get_distinct_country_list(self):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        my_sql = "SELECT distinct country from my_data_frame"

        my_return_data = psql.sqldf(my_sql)

        return_data = [ str(value).strip("[]'") for value in my_return_data.values.tolist()]
    
        return return_data





        






        


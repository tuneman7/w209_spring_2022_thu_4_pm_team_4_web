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
from  libraries.utility import Utility



class import_export_data(Utility):
    
    ALL_COUNTRIES_DATA_FRAME = None
    ALL_COUNTRIES_BY_TYPE_DF = None


    def __init__(self,load_data_from_url=False):
        super().__init__()
        global ALL_COUNTRIES_DATA_FRAME
        global ALL_COUNTRIES_BY_TYPE_DF
        if load_data_from_url == False:
            ALL_COUNTRIES_DATA_FRAME = self.load_and_clean_up_top_20_file()
            ALL_COUNTRIES_BY_TYPE_DF = self.load_and_clean_up_WTO_file()
        else:
            ALL_COUNTRIES_DATA_FRAME = self.load_and_clean_up_top_20_file_fromurl()
            ALL_COUNTRIES_BY_TYPE_DF = self.load_and_clean_up_WTO_file_fromurl()


    def print_internal_directory(self):

        for k,v in self.__dict__.items():
            print("{} is \"{}\"".format(k,v))

    def get_top_20_full_file_name(self) :

        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        top_20_file_name = "top20_2014-2020_all.csv"

        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,top_20_file_name)

        return return_file_name

    def get_WTO_full_file_name(self) :

        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        WTO_file_name = "WtoData_all.csv"

        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,WTO_file_name)

        return return_file_name

    def get_world_countries_by_iso_label(self):
        data_directory = "data"
        file_name = "countries.tsv"

        load_file_name = os.path.join(self.get_this_dir(),data_directory,file_name)

        my_data = pd.read_csv(load_file_name,sep='\t')
        return my_data

    def load_and_clean_up_top_20_file_fromurl(self):

        #url = "https://tuneman7.github.io/WtoData_all.csv"
        url = "https://tuneman7.github.io/top20_2014-2020_all.csv"

        my_data = pd.read_csv(url)
        
        return my_data


    def load_and_clean_up_top_20_file(self):

        file_to_load = self.get_top_20_full_file_name()

        my_data = pd.read_csv(file_to_load)
        
        return my_data

    def load_and_clean_up_WTO_file(self):

        file_to_load = self.get_WTO_full_file_name()

        my_data = pd.read_csv(file_to_load)
        
        return my_data

    def load_and_clean_up_WTO_file_fromurl(self):

        url = "https://tuneman7.github.io/WtoData_all.csv"
        #url = "https://tuneman7.github.io/top20_2014-2020_all.csv"

        my_data = pd.read_csv(url)
        
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

    def get_top5data_by_source_country(self,source_country):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        if source_country.lower() == 'world':
            my_sql = '''
            SELECT * 
            FROM (
                SELECT *,
                    RANK() OVER(PARTITION BY year ORDER BY [Total Trade ($M)] DESC) AS rnk
                FROM my_data_frame
                where country in (select distinct country from my_data_frame)
            ) t
            WHERE rnk <= 5
            '''
        else:

            my_sql = '''
            SELECT * 
            FROM (
                SELECT *,
                    RANK() OVER(PARTITION BY year ORDER BY [Total Trade ($M)] DESC) AS rnk
                FROM my_data_frame
                WHERE country = ''' + "'" + source_country + '''\'
            ) t
            WHERE rnk <= 5
            '''

        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def get_top5data_by_imports_exports(self,source_country, direction):

        global ALL_COUNTRIES_BY_TYPE_DF

        my_data_frame = ALL_COUNTRIES_BY_TYPE_DF
        if source_country.lower() != "world":
            my_sql = '''
            SELECT *
            FROM (
                SELECT 
                    Year, Value,
                    [Product/Sector-reformatted],
                    RANK() OVER(
                        PARTITION BY Year 
                        ORDER BY Value DESC) AS rnk
                FROM my_data_frame
                WHERE      
                    [Reporting Economy] =  \'''' + source_country + '''\'
                and
                    Direction = \'''' + direction + '''\'
                and
                    [Product/Sector-reformatted] NOT LIKE '%Total%'
            ) t
            WHERE rnk <= 5
            '''
        else:
            my_sql = '''
            SELECT *
            FROM (
                SELECT 
                    Year, Value,
                    [Product/Sector-reformatted],
                    RANK() OVER(
                        PARTITION BY Year 
                        ORDER BY Value DESC) AS rnk
                FROM my_data_frame
                WHERE      
                    [Reporting Economy] in (select distinct [Reporting Economy] from my_data_frame)
                and
                    Direction = \'''' + direction + '''\'
                and
                    [Product/Sector-reformatted] NOT LIKE '%Total%'
            ) t
            WHERE rnk <= 5
            '''


        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def get_top_trading_and_net_value(self,source_country):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME
        if source_country.lower() != "world":
            my_sql = '''
            SELECT 
            [Trading Partner],
            [year],
            [Total Trade ($M)],
            [Exports ($M)]-[Imports ($M)] as net_trade,
            'Net: ' || '$' || printf("%,d",cast([Exports ($M)]-[Imports ($M)] as text)) as net_trade_text,
            [Exports ($M)],
            [Imports ($M)],
            ''' + "'" + source_country + "'" + ''' as 'source_country'
            FROM (
                SELECT *,
                    RANK() OVER(PARTITION BY year ORDER BY [Total Trade ($M)] DESC) AS rnk
                FROM my_data_frame
                WHERE country = ''' + "'" + source_country + '''\'
            ) t
            WHERE rnk <= 5
            '''
        else:
            my_sql = '''
            SELECT 
            distinct
            [Trading Partner],
            [year],
            [Total Trade ($M)],
            [Exports ($M)]-[Imports ($M)] as net_trade,
            'Net: ' || '$' || printf("%,d",cast([Exports ($M)]-[Imports ($M)] as text)) as net_trade_text,
            [Exports ($M)],
            [Imports ($M)],
            'World' as source_country
            FROM (
                SELECT 
                    [Trading Partner],
                    sum([Total Trade ($M)]) as [Total Trade ($M)],
                    sum([Exports ($M)]) as [Exports ($M)],
                    sum([Imports ($M)]) as [Imports ($M)],
                    year,
                    RANK() OVER(PARTITION BY year ORDER BY sum([Total Trade ($M)]) DESC) AS rnk
                FROM my_data_frame
                WHERE country in (select distinct country from my_data_frame )
                --and [Trading Partner] <> 'European Union'
                group by [Trading Partner],year
            ) t
            WHERE rnk <= 5
            group by [Trading Partner], [year]            
            '''            

        my_return_data = psql.sqldf(my_sql)

        return my_return_data

        

    def get_distinct_country_list(self):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        my_sql = "SELECT distinct country from my_data_frame"

        my_return_data = psql.sqldf(my_sql)

        return_data = [ str(value).strip("[]'") for value in my_return_data.values.tolist()]
    
        return return_data

    def get_distinct_country_tuples(self):

        return [(value,value) for value in self.get_distinct_country_list()]





        






        


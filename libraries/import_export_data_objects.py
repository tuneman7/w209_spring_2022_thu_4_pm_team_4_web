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
    ALL_COUNTRIES_GDP_DATA = None
    EXCHANGE_RATE_DATA = None


    def __init__(self,load_data_from_url=False):
        super().__init__()
        global ALL_COUNTRIES_DATA_FRAME
        global ALL_COUNTRIES_BY_TYPE_DF
        global ALL_COUNTRIES_GDP_DATA
        global EXCHANGE_RATE_DATA
        if load_data_from_url == False:
            EXCHANGE_RATE_DATA = self.load_exchange_rate_data()
            ALL_COUNTRIES_DATA_FRAME = self.load_and_clean_up_top_20_file()
            ALL_COUNTRIES_BY_TYPE_DF = self.load_and_clean_up_WTO_file()
            ALL_COUNTRIES_GDP_DATA = self.load_and_clean_up_GDP_file()
            
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
    def get_GDP_full_file_name(self):
        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        GDP_file_name = "wb_econind_gdp_data.csv"
        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,GDP_file_name)

        return return_file_name


    def get_WTO_full_file_name(self) :

        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        WTO_file_name = "WtoData_all.csv"

        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,WTO_file_name)

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

    def get_exchange_rate_files(self) :

        data_directory = "data"
        exchange_rate_dir = "exchange_rates"
        exchange_rate = "exchange_rates_from_oecd_website.csv"
        country_codes = "wikipedia-iso-country-codes.csv"

        exchange_rate_file = os.path.join(self.get_this_dir(),data_directory,exchange_rate_dir,exchange_rate)

        country_code_file = os.path.join(self.get_this_dir(),data_directory,exchange_rate_dir,country_codes)

        return exchange_rate_file, country_code_file

    def load_exchange_rate_data(self):

        exchange_rate_file, country_code_file = self.get_exchange_rate_files()

        exchange_rates = pd.read_csv(exchange_rate_file)

        country_codes = pd.read_csv(country_code_file)

        mysql = '''
            select 
                country_codes.[English short name lower case] as Country,
                exchange_rates.TIME as year,
                exchange_rates.Value as rate
            from 
                exchange_rates
            join country_codes
                on
                country_codes.[Alpha-3 code] = exchange_rates.LOCATION

        '''

        return psql.sqldf(mysql)
        


    def load_and_clean_up_top_20_file_fromurl(self):

        #url = "https://tuneman7.github.io/WtoData_all.csv"
        url = "https://tuneman7.github.io/top20_2014-2020_all.csv"

        my_data = pd.read_csv(url)
        
        return my_data


    def load_and_clean_up_top_20_file(self):

        global EXCHANGE_RATE_DATA

        file_to_load = self.get_top_20_full_file_name()

        my_data = pd.read_csv(file_to_load)

        sql = '''
            select 
                my_data.*,
                EXCHANGE_RATE_DATA_1.rate as country_exchange_rate,
                EXCHANGE_RATE_DATA_2.rate as trading_partner_exchange_rate
            from my_data
            join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_1
                on
                    EXCHANGE_RATE_DATA_1.year = my_data.year
                and
                    EXCHANGE_RATE_DATA_1.Country = my_data.Country
            join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_2
                on
                    EXCHANGE_RATE_DATA_2.year = my_data.year
                and
                    EXCHANGE_RATE_DATA_2.Country = my_data.[Trading Partner]

        '''
        my_data = psql.sqldf(sql)
        
        return my_data

    def load_and_clean_up_GDP_file(self):

        file_to_load = self.get_GDP_full_file_name()

        my_data = pd.read_csv(file_to_load)

        global EXCHANGE_RATE_DATA

        sql = '''
        select 
            my_data.*,
            EXCHANGE_RATE_DATA.rate as exchange_rate
        from my_data
        left join EXCHANGE_RATE_DATA
            on 
                EXCHANGE_RATE_DATA.Country = my_data.Country
            and
                EXCHANGE_RATE_DATA.year = my_data.Year


        '''
        
        return psql.sqldf(sql)


    def load_and_clean_up_WTO_file(self):

        file_to_load = self.get_WTO_full_file_name()

        my_data = pd.read_csv(file_to_load)

        global EXCHANGE_RATE_DATA

        sql = '''
            select 
                my_data.*,
                EXCHANGE_RATE_DATA_1.rate as reporting_economy_exchange_rate,
                EXCHANGE_RATE_DATA_2.rate as partner_economy_exchange_rate
            from my_data
            left join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_1
                on
                EXCHANGE_RATE_DATA_1.Country = my_data.[Reporting Economy]
            left join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_2
                on
                EXCHANGE_RATE_DATA_2.Country = my_data.[Partner Economy]

        '''
        
        return psql.sqldf(sql)

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
            sum([Total Trade ($M)])  [Total Trade ($M)],
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

    def imports_exports_by_sectors(self,source_country, target_country, direction):

        global ALL_COUNTRIES_BY_TYPE_DF

        my_data_frame = ALL_COUNTRIES_BY_TYPE_DF
        if source_country.lower() != "world":
            my_sql = '''
            SELECT 
                Year, Value,
                [Product/Sector-reformatted],
                [Reporting Economy]
            FROM my_data_frame
            WHERE      
                ([Reporting Economy] =  \'''' + source_country + '''\'
                or
                [Reporting Economy] =  \'''' + target_country + '''\'
                )
            and
                Direction = \'''' + direction + '''\'
            and
                [Product/Sector-reformatted] NOT LIKE '%Total%'
            '''
        else:
            my_sql = '''
            SELECT 
                Year, Value,
                [Product/Sector-reformatted],
                [Reporting Economy]
            FROM my_data_frame
            WHERE      
                [Reporting Economy] in (select distinct [Reporting Economy] from my_data_frame)
            and
                Direction = \'''' + direction + '''\'
            and
                [Product/Sector-reformatted] NOT LIKE '%Total%'
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

        

    def get_distinct_country_list(self,add_world=False):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        my_sql = "SELECT distinct country from my_data_frame"

        my_return_data = psql.sqldf(my_sql)

        return_data = [ str(value).strip("[]'") for value in my_return_data.values.tolist()]
        if add_world == True:
            return_data.append("World")
    
        return return_data

    def get_distinct_country_tuples(self,add_world=False):

        return [(value,value) for value in self.get_distinct_country_list(add_world=add_world)]

    def get_gdp_data_by_country(self,source_country):

        global ALL_COUNTRIES_GDP_DATA

        my_data = ALL_COUNTRIES_GDP_DATA

        sql = "select * from my_data where Country = '" + source_country + "'"

        my_return = psql.sqldf(sql)

        return my_return
    
    def get_gdp_data_compare(self,source_country,target_country):

        global ALL_COUNTRIES_GDP_DATA

        my_data = ALL_COUNTRIES_GDP_DATA

        sql = "SELECT * FROM my_data WHERE Country = '" +  source_country + "' or Country = '" + target_country + "' "

        my_return = psql.sqldf(sql)

        return my_return

    def get_gdp_all_data(self):

        global ALL_COUNTRIES_GDP_DATA

        my_data = ALL_COUNTRIES_GDP_DATA

        sql = "SELECT * FROM my_data"

        my_return = psql.sqldf(sql)

        return my_return

    def get_Chinadata_by_country(self):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        my_sql = '''
        SELECT *,
            SUM(total_trade) OVER (PARTITION BY country, year) as total_toWorld_trade,
            SUM(exports) OVER (PARTITION BY country, year) as total_toWorld_exports,
            SUM(imports) OVER (PARTITION BY country, year) as total_toWorld_imports,
            SUM(net_exports) OVER (PARTITION BY country, year) as total_toWorld_net_exports
        FROM (
            SELECT
                country,
                year,
                SUM([Total Trade ($M)]) as total_trade,
                SUM([Exports ($M)]) as exports,
                SUM([Net Exports ($M)]) as net_exports,
                SUM([Imports ($M)]) as imports,
                CASE
                    WHEN [Trading Partner] = "China" THEN "China"
                    ELSE "Others"
                END as isChinaPartner
            FROM my_data_frame
            where country <> "China"
            GROUP BY isChinaPartner, country, year) t
        '''
        
        my_return_data = psql.sqldf(my_sql)
        return my_return_data







        






        


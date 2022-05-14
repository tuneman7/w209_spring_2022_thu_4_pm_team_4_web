from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.altair_renderings import AltairRenderings
from libraries.utility import Utility 
import socket 
def main():

    imp_object = Import_Export_Data()

    # print(imp_object.get_data_by_source_and_target_country(source_country='China',target_country='World'))

    # print(imp_object.get_data_by_source_and_target_country(source_country='Australia',target_country='China'))
    #print(imp_object.get_distinct_country_list())
    # print(imp_object.get_top5data_by_imports_exports("United States", 'exports'))
    # print(imp_object.get_top5data_by_imports_exports("United States", 'imports'))
    # print(imp_object.get_top_trading_and_net_value("world"))
    #print(imp_object.load_exchange_rate_data().head(3))
    #print(imp_object.load_exchange_rate_data())
    #print(imp_object.get_top_20_gdp_data_for_map())

    #my_altair = AltairRenderings()
    #my_altair.china_trade_war_slide_three()

    my_util = Utility()
    print(my_util.get_this_dir())
    print(socket.gethostname())

main()





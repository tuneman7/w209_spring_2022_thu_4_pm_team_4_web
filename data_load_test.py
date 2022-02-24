from libraries.import_export_data_objects import import_export_data as Import_Export_Data

def main():

    imp_object = Import_Export_Data()

    print(imp_object.get_data_by_source_and_target_country(source_country='China',target_country='World'))

    print(imp_object.get_data_by_source_and_target_country(source_country='Australia',target_country='China'))
    print(imp_object.get_distinct_country_list())
    print(imp_object.get_top5data_by_imports_exports("United States", 'exports'))
    print(imp_object.get_top5data_by_imports_exports("United States", 'imports'))
    print(imp_object.get_top_trading_and_net_value("world"))


main()


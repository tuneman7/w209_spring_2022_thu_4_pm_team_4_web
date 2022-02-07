from libraries.import_export_data_objects import import_export_data as Import_Export_Data

def main():

    imp_object = Import_Export_Data()

    print(imp_object.get_data_by_source_and_target_country(source_country='China',target_country='World'))

    print(imp_object.get_data_by_source_and_target_country(source_country='Australia',target_country='China'))



main()


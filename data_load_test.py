from libraries.import_export_data_objects import import_export_data as Import_Export_Data

def main():

    imp_object = Import_Export_Data()

    print(imp_object.load_and_clean_up_top_20_file())



main()


"""
Loads raw files and places in database
"""
import sys
import glob as glob
import helper_functions as helper
import parse_milk_volume as milk_volume
import parse_weather as weather
import parse_classification as classification
import parse_genetics as genetics

def load_dataset(dataset_name, file_regex):
    """Gathers specified data files, parses data, and inserts into database."""
    files = glob.glob(f'./data/raw/{dataset_name}/{file_regex}')
    with helper.get_db_engine().connect() as connection:
        for data_file in files:
            try:
                print(f"Storing file: {data_file}")
                if dataset_name == 'milk-volumes':
                    volume_df = milk_volume.get_dataframe_from_file(data_file)
                    volume_df.to_sql(con=connection, name='milk_volume', if_exists='append')
                elif dataset_name == 'weather':
                    weather_df = weather.get_dataframe_from_file(data_file)
                    weather_df.to_sql(con=connection, name='weather', if_exists='append')
                elif dataset_name == 'classifications':
                    classification_df = classification.get_dataframe_from_file(data_file)
                    classification_df.to_sql(con=connection, name='classification', if_exists='append')
                elif dataset_name == 'genetics':
                    genetics_df = genetics.get_dataframe_from_file(data_file)
                    genetics_df.to_sql(con=connection, name='genetics', if_exists='append')
                else:
                    raise ValueError('Unhandled dataset')
            except Exception as e:
                print(e)
                print(f"Unable to parse {data_file}")
                print(f"Skipping file...")

def main():
    """ Loads local database """
    load_dataset('milk-volumes', '*.txt')
    load_dataset('weather', '*.csv')
    load_dataset('classifications', '*.csv')
    load_dataset('genetics', '*.csv')
    
if __name__ == '__main__':
    sys.exit(main())

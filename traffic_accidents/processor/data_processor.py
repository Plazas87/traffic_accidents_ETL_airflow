import pandas as pd
import googlemaps
import re


class DataProcessor:
    """This class contain all methods and properties used to process traffic-accidents before 2019"""
    def __init__(self):
        pass

    @staticmethod
    def fix_date(str_column=None):
        return pd.to_datetime(str_column, format='%d/%m/%Y')

    @staticmethod
    def fix_hour(row=None):
        """This function transform string hour representation into integer representation"""
        tmp = row.split(':')[0]
        tmp = int(tmp.replace('DE ', ''))
        return tmp

    @staticmethod
    def clean_white_spaces(data):
        for column_name in list(data.columns):
            try:
                data[column_name] = data[column_name].apply(lambda row: str.strip(row))

            except Exception as e:
                print(f'Error: {e}')
                continue

        return data

    @staticmethod
    def rename_columns(data):
        data.rename(columns={'Nº': 'street_number',
                             'Nº PARTE': 'numero_parte',
                             '* Nº VICTIMAS': 'numero_victimas'},
                    inplace=True)

        data.columns = data.columns.map(lambda name: str.lower(name).replace(' ', '_'))
        return data

    @staticmethod
    def geocode_direction(data):
        geocode_result = []
        with open('./docs/google_api_key.txt') as file:
            API_KEY = file.readline()

        gmaps = googlemaps.Client(key=API_KEY)

        # make a list of uniques id's for each accident
        accidents_by_parte = pd.unique(data.numero_parte)
        data_grouped = DataProcessor.group_by_data(data, ['numero_parte'])

        for index, parte in enumerate(accidents_by_parte):
            tmp_data = data_grouped.get_group(parte).copy()
            accident_direction = tmp_data.iloc[0, 4]
            street_num = tmp_data.iloc[0, 5]
            if not (re.search(r'KM.', accident_direction) or re.search(r'[a-zA-Z]-[0-9]', accident_direction) or re.search(r'ENTRADA', accident_direction)):
                try:
                    if re.search(r'NUM', accident_direction):
                        accident_direction = accident_direction + ', ' + street_num + ' MADRID'
                        print(f'Geocoding: {accident_direction} ...', end='')

                    else:
                        accident_direction = accident_direction + ', MADRID'
                        print(f'Geocoding: {accident_direction} ...', end='')

                    lat, lon = gmaps.geocode(accident_direction)[0]['geometry']['location'].values()
                    tmp_data['lat'] = lat
                    tmp_data['lon'] = lon
                    geocode_result.append(tmp_data)
                    print(' DONE')
                except Exception as e:
                    print('Error:', e)
                    continue

        return pd.concat(geocode_result)

    @staticmethod
    def group_by_data(data, column_names):
        return data.groupby(column_names)

from .mappers import Plotter
from helpers import FileReader
import pandas as pd


class Mapper:
    @staticmethod
    def heatmap():
        mapper = Plotter()
        reader = FileReader(module_path='processed_data')
        station_df = reader.read_csv_file('processed_data_2018.csv', separator=';')
        locations = station_df.iloc[:, [26, 27]].values
        mapper.add_traffic_heatmap(locations=locations)
        mapper.generate_map('traffic_accidents_heatmap_2018')

    @staticmethod
    def standard_map():
        mapper = Plotter()
        reader = FileReader(module_path='processed_data')
        station_df = reader.read_csv_file('processed_data_2018.csv', separator=';', encoding=['utf-8'])
        station_df = Mapper.prepare_data(station_df)
        station_df.apply(lambda row: mapper.add_accident(row), axis=1)
        mapper.generate_map('traffic_accidents_2018')

    @staticmethod
    def prepare_data(data):
        lista_partes = pd.unique(data.numero_parte)
        grouped_data = data.groupby('numero_parte')
        accidents_by_gender = []

        for index, parte in enumerate(lista_partes):
            tmp_data = grouped_data.get_group(parte)
            drivers = tmp_data[
                (tmp_data['tipo_accidente'] == 'COLISIÓN DOBLE') & (tmp_data['tipo_persona'] == 'CONDUCTOR')].copy()

            if len(drivers) == 2:
                accident = [parte, drivers.iloc[0, 0], drivers.iloc[0, 1], drivers.iloc[0, 2], drivers.iloc[0, 4],
                            drivers.iloc[0, 3], drivers.iloc[0, 26], drivers.iloc[0, 27], drivers.iloc[0, 20],
                            drivers.iloc[0, 22], drivers.iloc[0, 21], drivers.iloc[0, 23], drivers.iloc[0, 25],
                            drivers.iloc[1, 22],
                            drivers.iloc[1, 21], drivers.iloc[1, 23], drivers.iloc[1, 25]]

                accidents_by_gender.append(accident)

        processed_data = pd.DataFrame(accidents_by_gender,
                                      columns=[
                                          'numero_parte', 'fecha', 'hora', 'dia_semana', 'lugar', 'distrito',
                                          'lat', 'lon', 'tipo_accidente', 'conductor_1', 'conductor_1_tipo_vehiculo',
                                          'conductor_1_sexo', 'conductor_1_edad', 'conductor_2',
                                          'conductor_2_tipo_vehiculo', 'conductor_2_sexo', 'conductor_2_edad'])

        return processed_data





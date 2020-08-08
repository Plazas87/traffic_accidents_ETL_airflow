from helpers import FileReader
from .processor import DataProcessor


class Controller:
    """This class contains contains and manages all methods and properties to process traffic accidents data"""
    def __init__(self):
        self._status = False
        self.errors = []
        self.file_reader = FileReader()
        self.processor = DataProcessor()

    def run(self):
        self._process_data()

    def _update_status(self, value):
        self._status = value

    def _process_data(self):
        self._update_status(True)

        # clean data
        data = self._read_data('2018_Accidentalidad.csv', sep=';')
        data = self._clean_data(data)

        # process data
        data = self.processor.clean_white_spaces(data)
        data = self.processor.rename_columns(data)
        data = self.processor.geocode_direction(data)
        self.save_data(data)

    def _read_data(self, filename, sep):
        return self.file_reader.read_csv_file(file_name=filename, separator=sep)

    def _clean_data(self, data):
        data['FECHA'] = self.processor.fix_date(data['FECHA'])
        data['RANGO HORARIO'] = data['RANGO HORARIO'].apply(lambda row: self.processor.fix_hour(row))
        return data

    @staticmethod
    def save_data(data):
        data.to_csv('./traffic_accidents/resources/processed_data/processed_data_2018.csv',
                    sep=';',
                    header=True,
                    encoding='utf-8',
                    index=False)


if __name__ == '__main__':
    controller = Controller()
    controller.run()

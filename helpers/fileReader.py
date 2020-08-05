#!usr/bin/env python

import pandas as pd
from helpers import Encodings, Separators


class FileReader:
    def __init__(self, module_path='data', header='infer'):
        self._sep = Separators._value2member_map_.keys()
        self._header = header
        self._encoding = Encodings._value2member_map_.keys()
        self._data = []
        self._file_name = ''
        self._data_path = './traffic_accidents/resources/' + module_path + '/'

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if type(value) is str:
            self._file_name = value

        else:
            raise ValueError('The param "file_name" must be a string')

    @property
    def sep(self):
        return self._sep

    @sep.setter
    def sep(self, value):
        if (value == ',') or (value == ';') or (value == '\\t'):
            self._sep = value

        else:
            raise ValueError('sep param must be ",", ";" or a tab')

    @property
    def data(self):
        return self._data

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, value):
        if isinstance(value, str):
            self._data_path = value

        else:
            raise ValueError('Try to set data path with no str value')

    def read_csv_file(self, file_name, separator=None, encoding=None):
        path = self._data_path + file_name
        if separator is not None:
            self.sep = separator

        if encoding is not None:
            self._encoding = encoding

        data = []
        for sep in self.sep:
            if len(data) == 0:
                for encoding in self._encoding:
                    try:
                        print(f'Reading file {path} using: sep={sep} - encoding={encoding}')
                        data = pd.read_csv(path, sep=sep, header=self._header, encoding=encoding)
                        break

                    except pd.errors.ParserError as e:
                        print(f'Bad separator: {sep} - {e}')
                        break

                    except UnicodeDecodeError as e:
                        print(f'Bad encoding: {encoding} - {e}')
                        continue
                    except Exception as e:
                        print(f'Can´t read : - {e}')

        return data

    def __str__(self):
        return f'Separador: {self._sep}\n' + \
               f'Cabecera: {self._header}\nEncoding: {self._encoding}'


if __name__ == '__main__':
    pass

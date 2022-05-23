import pandas as pd


class Sorter:
    """
    Класс реализованный для сортировки фрейма по определенному полю
    """

    def __init__(self, document):
        self._document = document

    def get_sorted_data(self, key):
        frame = pd.read_excel(self._document.get_file_path())
        return frame.sort_values(str(key))


class Parser:
    """
    Класс для парсинга файлов
    """

    def __init__(self, document):
        self._document = document
        self._path = document.get_file_path()

    def get_sheet(self) -> list:
        """
        Метод возвращает все листы файла
        """

        xls = pd.ExcelFile(self._path)
        sheet = xls.sheet_names
        return sheet

    def parse(self) -> str:
        sheets = self.get_sheet()
        data = ""
        for page in sheets:
            frame = pd.read_excel(self._path, page)
            data += f'{page} \n {frame} \n'

        return str(data)

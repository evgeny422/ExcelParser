import datetime
import os

from django.core.exceptions import ValidationError
from openpyxl import load_workbook


class ParserToDatabase:
    """
        Класс для парсинга файлов "Я - как проект"
    """

    def __init__(self, document):
        self._document = document
        self._path = document.get_file_path()
        self.wb = load_workbook(self._path, read_only=True)
        self.sheetlist = self.wb.sheetnames

    def check_sheet(self):
        """
        Валидация файла по имеющимся листам
        """

        if {'ОБЩИЙ ПЛАН', 'Образование', 'Дело', 'Организация и коллектив', 'Репутация', 'Здоровье',
            'Семья и окружение'} != set(self.sheetlist):
            self.wb.close()
            self._document.delete()
            raise ValidationError('Нереверный макет файла!')
        return self.sheetlist

    def get_values_by_sheet(self):
        """
        Подсчет очков для каждой страницы
        """

        checklist = {}
        result = {}
        for page in self.check_sheet()[1:]:
            for v, _, _, _, _, _, c, i in self.wb[page]['H37':'O56']:

                if not checklist.get(str(page)):
                    checklist[str(page)] = {
                        'Задача': {v.value},
                        'Дедлайн': [c.value - datetime.datetime(2022, 2, 21, 0, 0)
                                    if isinstance(c.value, datetime.datetime)
                                    else datetime.timedelta(days=0)],
                        'Статус': [i.value]
                    }
                else:
                    checklist[str(page)]['Задача'].add(v.value)
                    checklist[str(page)]['Дедлайн'].append(
                        c.value - datetime.datetime(2022, 2, 21, 0, 0)
                        if isinstance(c.value, datetime.datetime) else datetime.timedelta(days=0))
                    checklist[str(page)]['Статус'].append(i.value)

            checklist[page]['Задача'].discard("' '")
            checklist[page]['Задача'].discard(None)

            result[page] = {
                'total_deadline': sum(checklist.get(page)['Дедлайн'], datetime.timedelta(0, 0)),
                'statuses': {i: checklist.get(page)['Статус'].count(i) for i in set(checklist.get(page)['Статус'])},
                'range_task': len(checklist.get(page)['Задача'])
            }
        self.wb.close()

        return result

    def get_sum_of_status(self, values: dict):
        """
        Подсчет итоговых баллов по статусу, в соответствии с правилами
        """

        points = {
            None: 0,
            'Выполнено': 2,
            'В процессе': 1,
            'Не начато': 0,
        }

        counter = 0

        for key in values.keys():
            for k, v in values.get(key)['statuses'].items():
                counter += points.get(k) * v
        return counter

    def get_total_values(self):
        """
        Возвращает суммарные очки за все разделы
        """
        sheet_values_list = self.get_values_by_sheet()
        res = {'deadline': 0, 'status': self.get_sum_of_status(sheet_values_list), 'task': 0}

        for i in sheet_values_list.keys():
            res['deadline'] += sheet_values_list[i]['total_deadline'].days
            res['task'] += sheet_values_list[i]['range_task']

        return res

import datetime
from openpyxl import load_workbook


class ParserToDatabase:
    """
        Класс для парсинга файлов
    """

    def __init__(self, document):
        self._document = document
        self._path = document.get_file_path()

    def get_values_by_sheet(self):
        """
        Подсчет очков для каждой страницы
        """

        wb = load_workbook(self._path, read_only=True)
        checklist = {}
        result = {}

        for page in wb.sheetnames[1:]:
            for v, _, _, _, _, _, c, i in wb[page]['H37':'O56']:

                if not checklist.get(str(page)):
                    checklist[str(page)] = {
                        'Задача': [1 if len(v.value) > 1 else 0],
                        'Дедлайн': [c.value - datetime.datetime(2022, 2, 21, 0, 0)
                                    if isinstance(c.value, datetime.datetime)
                                    else datetime.timedelta(days=0)],
                        'Статус': [i.value]
                    }
                else:
                    checklist[str(page)]['Задача'].append(1 if len(v.value) > 1 else 0)
                    checklist[str(page)]['Дедлайн'].append(
                        c.value - datetime.datetime(2022, 2, 21, 0, 0)
                        if isinstance(c.value, datetime.datetime) else datetime.timedelta(days=0))
                    checklist[str(page)]['Статус'].append(i.value)

            result[page] = {
                'total_deadline': sum(checklist.get(page)['Дедлайн'], datetime.timedelta(0, 0)),
                'statuses': {i: checklist.get(page)['Статус'].count(i) for i in set(checklist.get(page)['Статус'])},
                'range_task': sum(checklist.get(page)['Задача'])
            }
        wb.close()
        print(result)
        return result

    def get_total_values(self):
        """
        Возвращает суммарные очки
        """
        sheet_values_list = self.get_values_by_sheet()
        res = {'deadline': 0,
               'status': 0,
               'task': 0,
               }
        for i in sheet_values_list.keys():
            res['deadline'] += sheet_values_list[i]['total_deadline'].days
            res['task'] += sheet_values_list[i]['range_task']

        return res

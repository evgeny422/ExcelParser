import json
import os

from django.conf import settings

from ExcelParser.settings.base import BASE_DIR


def create_file_title():
    import datetime
    basename = "json_sample"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix])
    return filename


def generate_sample():
    dictionary = {
        'x': ['x', ],
        'y1': ['Статус', ],
        'y2': ['Дедлайн', ],
        'y3': ['План', ]
    }
    name = create_file_title()
    media_path = os.path.join(BASE_DIR, 'plot_engine/json_media')
    file_path = f"{os.path.join(media_path, f'{name}.json')}"
    open(f"{file_path}", 'w+')

    with open(f"{file_path}", 'w+') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)

    return file_path


def upload_data(file: str = None, time_delta: str = None, status_value: str = None, deadline_value: str = None,
                plan_value: str = None):
    # file_path = os.path.join(settings.BASE_DIR, *file.split('/'))

    with open(file) as f:
        data = json.load(f)

    with open(file, mode='w') as f:
        data['x'].append(str(time_delta))
        data['y1'].append(str(status_value))
        data['y2'].append(str(deadline_value))
        data['y3'].append(str(plan_value))
        json.dump(data, f, ensure_ascii=False, indent=4)

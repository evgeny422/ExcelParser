from django.core.exceptions import ValidationError


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    return True


def validate_content_of_file(self):
    if {'ОБЩИЙ ПЛАН', 'Образование', 'Дело', 'Организация и коллектив', 'Репутация', 'Здоровье',
        'Семья и окружение'} != set(self.sheetlist):
        self.wb.close()
        raise ValidationError('Нереверный макет файла!')
    return True

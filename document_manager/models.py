import json
from abc import abstractmethod

from django.conf import settings
from django.core.exceptions import FieldError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from document_manager.services.dataframes_services import ParserToDatabase
from document_manager.validators import validate_file_extension
from plot_engine.json_manager import generate_sample, upload_data


class DocumentAbstract:
    """
    Интерфейс модели Document
    """

    @abstractmethod
    def get_file_path(self):
        pass

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_content(self):
        pass


class Event(models.Model):
    """
    Событие - начало подстчета баллов
    """
    title = models.CharField('Название мероприятия', max_length=150, unique=True)

    outdated = models.BooleanField('Доступно в истории просмотров', default=False)
    current = models.BooleanField('Текущее', default=True)

    day = models.PositiveSmallIntegerField('День')
    month = models.PositiveSmallIntegerField('Месяц')
    year = models.PositiveSmallIntegerField('Год')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'Событие'

    def get_absolute_url(self):
        return reverse("documents_event_slug", kwargs={"slug": self.title})

    def __str__(self):
        return f'{self.title}'


class Document(DocumentAbstract, models.Model):
    """
    Модель документа
    """
    title = models.CharField('Название', max_length=200)
    uploaded_file = models.FileField('Файл', upload_to="media/", validators=[validate_file_extension, ])
    date_time_of_added = models.DateTimeField('Время добавления', auto_now=True)
    date_time_of_updated = models.DateTimeField('Время обновления', blank=True, null=True)
    content = models.TextField('Содержание', blank=True)

    deadline_ratio = models.IntegerField('Дедлайн', blank=True, null=True)
    status_ratio = models.IntegerField('Статус', blank=True, null=True)
    action_plan_ratio = models.IntegerField('План действий', blank=True, null=True)

    password = models.CharField('Пароль', max_length=150)
    json_file_path = models.CharField('json', max_length=250, blank=True)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    _file_json = None

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документ'

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self._file_json = self.get_file_json()

    def get_file_path(self):
        if self.uploaded_file.path:
            return f"{self.uploaded_file.path}"

        return self.uploaded_file.url

    def get_file_json(self):
        if self._file_json:
            return self._file_json
        file_path = self.json_file_path
        if settings.DEBUG:
            file_path = f'{settings.BASE_DIR}{file_path}'
        if file_path:
            with open(file_path) as f:
                return json.load(f, )
        return {}

    def deadline_changed_ratio(self):
        data = self.get_file_json()
        is_changed = len(data['y2']) > 1
        if is_changed:
            prev_deadline = data['y2'][len(data['y2']) - 2]
            return self.deadline_ratio - int(prev_deadline)
        return 0

    def status_changed_ratio(self):
        data = self.get_file_json()
        is_changed = len(data['y1']) > 1
        if is_changed:
            prev_status = data['y1'][len(data['y1']) - 2]
            return self.status_ratio - int(prev_status)
        return 0

    def action_changed_ratio(self):
        data = self.get_file_json()
        is_changed = len(data['y3']) > 1
        if is_changed:
            prev_action = data['y3'][len(data['y3']) - 2]
            return self.action_plan_ratio - int(prev_action)
        return 0

    def get_title(self):
        return f"{self.title}"

    def get_content(self):
        return f"{self.content}"

    def save(self, *args, **kwargs):
        """
        Сохранение в БД значений суммарных очков  после парсинга документа
        """

        if not self.uploaded_file:
            raise FieldError('Не передан файл')
        if validate_file_extension(self.uploaded_file):
            super().save(*args, **kwargs)
        try:
            pars = ParserToDatabase(self).get_total_values()
            self.content = 'Content'
            self.deadline_ratio = abs(pars.get('deadline', 0) // 10)
            self.status_ratio = pars.get('status', 0)
            self.action_plan_ratio = pars.get('task', 0)
            self.date_time_of_updated = now()
        except:
            self.delete()
            raise FieldError('Некорректный файл')

        if self.json_file_path:
            self.json_file_path = self.json_file_path
        else:
            self.json_file_path = generate_sample()

        upload_data(
            file=self.json_file_path,
            time_delta=self.date_time_of_updated.date(),
            status_value=self.status_ratio,
            deadline_value=self.deadline_ratio // 10,
            plan_value=self.action_plan_ratio
        )

        return super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

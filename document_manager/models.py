from abc import abstractmethod

from django.core.exceptions import FieldError
from django.db import models
from django.utils.timezone import now

from document_manager.services.dataframes_services import ParserToDatabase
from document_manager.validators import validate_file_extension


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

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документ'

    def get_file_path(self):
        if self.uploaded_file.path:
            return f"{self.uploaded_file.path}"

        return self.uploaded_file.url

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
        pars = ParserToDatabase(self).get_total_values()
        self.content = 'Content'
        self.deadline_ratio = pars.get('deadline', 0)
        self.status_ratio = pars.get('status', 0)
        self.action_plan_ratio = pars.get('task', 0)
        self.date_time_of_updated = now()

        return super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

from abc import abstractmethod

from django.db import models

from document_manager.services.dataframes_services import Parser


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
    title = models.CharField(max_length=200)
    uploaded_file = models.FileField(upload_to="media/")
    date_time_of_added = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)

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
        super().save(*args, **kwargs)
        parser = Parser(self)
        if (not self.content) or (not self.pk):
            self.content = parser.parse()
        return super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

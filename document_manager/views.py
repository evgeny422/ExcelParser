import json
import os

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.views.generic import ListView

from ExcelParser.settings_dev import INITIAL_FILE_PATH_
from document_manager.forms import DocumentUpdateForm, DocumentForm
from document_manager.models import Document, Event


class DocumentsList(ListView):
    """ Список всех имеющихся документов """

    model = Document
    event = Event.objects.filter(outdated=True)
    queryset = Document.objects.filter(event__current=True).values('pk', 'title', 'deadline_ratio', 'status_ratio',
                                                                   'action_plan_ratio')
    template_name = 'documents/document_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['update_form'] = DocumentUpdateForm
        return context


class DocumentDetail(View):
    """Информация об отдельном документе"""

    def get(self, request, *args, **kwargs):
        doc = get_object_or_404(Document, pk=kwargs['pk'])
        file_path = doc.json_file_path
        if settings.DEBUG and file_path:
            file_path = f'{settings.BASE_DIR}{file_path}'
        with open(file_path) as f:
            data = json.load(f, )

        return render(request, 'documents/document_detail.html',
                      context={'document': doc, 'data': data})


class DocumentFromEvent(View):
    """Документы в зависимости от события"""

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(title=kwargs['slug'])
        if event.outdated:
            document_list = Document.objects.filter(event=event.pk)
            return render(request, template_name='documents/document_event_list.html', context={
                'document_list': document_list,
                'event_name': event.title
            })
        else:
            raise Http404


class DocumentEventSort(View):
    """Сортировка документов по ключу, где ключ - столбец в файле"""

    template_name = 'documents/document_list.html'

    def get(self, request, *args, **kwargs):
        print(kwargs)
        values = {
            'Дедлайн': 'deadline_ratio',
            'Статус': 'status_ratio',
            'План действий': 'action_plan_ratio',
        }
        key = self.request.GET.get("orderby").strip()
        if key in values.keys():
            key = values.get(key)

        document_list = Document.objects.filter(event__title=kwargs['slug']).order_by(key)
        event = Event.objects.get(title=kwargs['slug'])
        return render(request, template_name='documents/document_event_list.html', context={
            'document_list': document_list,
            'event_name': event.title
        })

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["key"] = self.request.GET.get("key")
        return context


class DocumentEventSearch(View):
    """Поиск документов конкретного события"""

    def get(self, request, *args, **kwargs):
        document_list = Document.objects.filter(
            title__icontains=self.request.GET.get("q").strip(),
            event__outdated=True
        )
        event = Event.objects.get(title=kwargs.get('slug'))
        return render(request, template_name='documents/document_event_list.html', context={
            'document_list': document_list,
            'event_name': event.title
        })


class DocumentSort(ListView):
    """Сортировка документов по ключу, где ключ - столбец в файле"""

    template_name = 'documents/document_list.html'

    def get_queryset(self):
        values = {
            'Дедлайн': 'deadline_ratio',
            'Статус': 'status_ratio',
            'План действий': 'action_plan_ratio',
        }
        key = self.request.GET.get("orderby").strip()
        if key in values.keys():
            key = values.get(key)

        return Document.objects.filter(event__outdated=True).order_by(key)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["key"] = self.request.GET.get("key")
        return context


class DocumentSearch(ListView):
    """Поиск задачи по url"""
    template_name = 'documents/document_list.html'

    def get_queryset(self):
        return Document.objects.filter(title__icontains=self.request.GET.get("q").strip(),
                                       event__outdated=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context


class DocumentAdd(View):
    """
    Добавление документов в БД
    """

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('documents')

        return render(request, 'documents/message.html', {'message': form.errors})


class DocumentDownload(View):
    """
    Дает возможность пользователю скачать файл
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Document, pk=kwargs['pk'])
        filename = obj.uploaded_file.path
        response = FileResponse(open(filename, 'rb'))
        return response


class DocumentDelete(View):
    """
    Дает возможность пользователю удалить файл
    """

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        obj = get_object_or_404(Document, pk=kwargs['pk'])
        try:
            os.remove(obj.get_file_path())
        except:
            pass
        obj.delete()
        return redirect('documents')


class DocumentUpdate(View):
    """
    Обновление документа
    """

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Document, pk=kwargs['pk'])
        path = obj.get_file_path()
        form = DocumentUpdateForm(request.POST, request.FILES, instance=obj, )

        if form.is_valid():
            form.save()
            try:
                os.remove(path)
            except:
                pass

            return redirect('documents')

        return render(request, 'documents/document_detail.html', {'message': form.errors, 'document': obj})


class DownloadInitialFile(View):
    """
    Оригинальный файл "Я - как проект"
    """

    def get(self, request, *args, **kwargs):
        filename = INITIAL_FILE_PATH_
        return FileResponse(open(filename, 'rb'))


class DocumentHistory(View):
    """
    Отображение истории добаления файлов по мероприятиям
    """

    def get(self, request, *args, **kwargs):
        event = get_list_or_404(Event)

        return render(request, template_name='documents/document_history.html', context={
            'events': event
        })

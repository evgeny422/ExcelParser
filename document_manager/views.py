import os

from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from ExcelParser.settings import BASE_DIR
from document_manager.forms import DocumentUpdateForm, DocumentForm
from document_manager.models import Document


class DocumentsList(ListView):
    """ Список всех имеющихся документов """

    model = Document
    queryset = Document.objects.values('pk', 'title', 'deadline_ratio', 'status_ratio', 'action_plan_ratio')
    template_name = 'documents/document_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['update_form'] = DocumentUpdateForm

        return context


class DocumentDetail(View):
    """Информация об отдельном документе"""

    def get(self, request, *args, **kwargs):
        doc = get_object_or_404(Document, pk=kwargs['pk'])
        return render(request, 'documents/document_detail.html', context={'document': doc})


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

        return Document.objects.order_by(key)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["key"] = self.request.GET.get("key")
        return context


class DocumentSearch(ListView):
    """Поиск задачи по url"""
    template_name = 'documents/document_list.html'

    def get_queryset(self):
        return Document.objects.filter(title__icontains=self.request.GET.get("q").strip())

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

        return render(request, 'documents/message.html', {'message': form.errors})


class DownloadInitialFile(View):
    """
    Оригинальный файл "Я - как проект"
    """

    def get(self, request, *args, **kwargs):
        filename = os.path.join(BASE_DIR, 'initial_excel_files/Журнал_Я_как_проект_ШР21_верная_версия.xlsx')
        response = FileResponse(open(filename, 'rb'))
        return response

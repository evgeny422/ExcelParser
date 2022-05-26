import os

from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from document_manager.forms import DocumentUpdateForm
from document_manager.models import Document


class DocumentsList(ListView):
    """ Список всех имеющихся документов """

    model = Document
    queryset = Document.objects.values('pk', 'title', 'deadline_ratio', 'status_ratio', 'action_plan_ratio')
    template_name = 'documents/document_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['update_form'] = DocumentUpdateForm()
        return context


class DocumentDetail(View):
    """Информация об отдельном документе"""

    def get(self, request, *args, **kwargs):
        doc = Document.objects.get(id=kwargs['pk'])
        return render(request, 'documents/document_detail.html', context={'document': doc})


class DocumentSort(ListView):
    """Сортировка документов по ключу, где ключ - столбец в файле"""

    template_name = 'documents/document_list.html'

    def get_model_field(self, value):
        values = {
            'Дедлайн': 'deadline_ratio',
            'Статус': 'status_ratio',
            'План действий': 'action_plan_ratio',

        }
        return values.get(value)

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
        file = request.FILES.get('File')
        file_name = request.POST.get('File_title')
        password = request.POST.get('password')
        document = Document(
            title=file_name,
            uploaded_file=file,
            password=password,
        )
        document.save()

        return redirect('documents')


class DocumentDownload(View):
    """
    Дает возможность пользователю скачать файл
    """

    def get(self, request, *args, **kwargs):
        obj = Document.objects.get(id=kwargs['pk'])
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
        obj = Document.objects.get(id=kwargs['pk'])
        path = obj.get_file_path()
        os.remove(path)
        obj.delete()
        return redirect('documents')


class DocumentUpdate(View):
    """
    Обновление документа
    """

    def post(self, request, *args, **kwargs):
        obj = Document.objects.get(pk=kwargs['pk'])
        path = obj.get_file_path()
        form = DocumentUpdateForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            form.save()
            os.remove(path)
            return redirect('documents')
        # if obj.password.strip() != request.POST.get('password'):
        #     raise PermissionDenied
        # file, file_name = request.FILES.get('uploaded_file'), request.POST.get('title')
        # obj.title, obj.uploaded_file = file_name, file
        #
        # obj.save()

        return render(request, 'documents/message.html', {'message': 'Введен неверный пароль'})

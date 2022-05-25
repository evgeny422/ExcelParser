from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from document_manager.models import Document


class DocumentsList(ListView):
    """ Список всех имеющихся документов """

    model = Document
    queryset = Document.objects.values('pk', 'title', 'deadline_ratio', 'status_ratio', 'action_plan_ratio')
    template_name = 'documents/document_list.html'


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
        key = self.get_model_field(value=self.request.GET.get("orderby").strip())
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
        document = Document(
            title=file_name,
            uploaded_file=file,
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
    Дает возможность пользователю скачать файл
    """

    def get(self, request, *args, **kwargs):
        obj = Document.objects.get(id=kwargs['pk'])
        obj.delete()
        return redirect('documents')


class DocumentUpdate(View):
    def post(self, request, *args, **kwargs):
        obj = Document.objects.get(pk=kwargs['pk'])
        file = request.FILES.get('File')
        file_name = request.POST.get('File_title')
        obj.title = file_name
        obj.uploaded_file = file
        obj.save()

        return redirect('documents')

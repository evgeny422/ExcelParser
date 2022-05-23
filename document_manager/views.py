from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from document_manager.models import Document


class DocumentsList(ListView):
    """ Список всех имеющихся документов """

    model = Document
    queryset = Document.objects.values('pk', 'title')
    template_name = 'documents/document_list.html'


class DocumentDetail(DetailView):
    """Информация об отдельном документе"""

    model = Document


class DocumentSort(View):
    """Сортировка документов по ключу, где ключ - столбец в файле"""

    def get(self, request, key=None):
        pass


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

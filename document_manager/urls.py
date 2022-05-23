from django.urls import path

from document_manager.views import DocumentsList, DocumentAdd, DocumentSearch

urlpatterns = [

    path('', DocumentsList.as_view(), name='documents'),
    path('search/', DocumentSearch.as_view(), name='search'),
    path('add_document/', DocumentAdd.as_view(), name='add_document'),
]
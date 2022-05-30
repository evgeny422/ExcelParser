from django.urls import path

from document_manager.views import DocumentsList, DocumentAdd, DocumentSearch, DocumentDetail, DocumentSort, \
    DocumentDownload, DocumentDelete, DocumentUpdate, DownloadInitialFile

urlpatterns = [

    path('', DocumentsList.as_view(), name='documents'),
    path('download_initial_file/', DownloadInitialFile.as_view(), name='initial_file'),
    path('search/', DocumentSearch.as_view(), name='search'),
    path('add_document/', DocumentAdd.as_view(), name='add_document'),
    path('sort_documents/', DocumentSort.as_view(), name='sorted_documents'),
    path('<int:pk>/', DocumentDetail.as_view(), name='document'),
    path('download/<int:pk>/', DocumentDownload.as_view(), name='download'),
    path('delete/<int:pk>/', DocumentDelete.as_view(), name='delete'),
    path('update/<int:pk>/', DocumentUpdate.as_view(), name='update'),


]

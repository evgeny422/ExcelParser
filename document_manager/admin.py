from django.contrib import admin
from django.forms import ModelForm, CharField

from document_manager.models import Document
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class DocumentAdminForm(ModelForm):
    content = CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Document
        fields = "__all__"


@admin.register(Document)
class DocumentAdminModel(admin.ModelAdmin):
    list_display = ('pk', 'title', 'date_time_of_added',)
    list_display_links = ('pk', 'title')
    search_fields = ['date_time_of_added', 'title', ]
    ordering_fields = ('pk', 'title')
    #form = DocumentAdminForm

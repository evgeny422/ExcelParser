from django.contrib import admin
from django.forms import ModelForm, CharField

from document_manager.models import Document, Event


@admin.register(Document)
class DocumentAdminModel(admin.ModelAdmin):
    list_display = ('pk', 'title', 'date_time_of_added',)
    list_display_links = ('pk', 'title')
    search_fields = ['date_time_of_added', 'title', ]
    ordering_fields = ('pk', 'title')
    # form = DocumentAdminForm


@admin.register(Event)
class DocumentAdminModel(admin.ModelAdmin):
    list_display = ('pk', 'title', "outdated", 'current')
    list_display_links = ('pk', 'title')
    search_fields = ['title', ]
    ordering_fields = ('pk', 'title')
    list_editable = ["outdated", "current"]

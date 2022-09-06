from django import template

from document_manager.models import Event

register = template.Library()


@register.simple_tag
def get_categories():
    return Event.objects.all()

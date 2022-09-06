from document_manager.models import Event


def get_categories():
    return {'events': Event.objects.all()}

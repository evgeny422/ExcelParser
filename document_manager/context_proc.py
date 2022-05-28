from document_manager.forms import DocumentUpdateForm
from document_manager.views import DocumentAdd


def document_update_form(request):
    return {"formDocUpdate": DocumentUpdateForm}


def document_add_form(request):
    return {'document_form': DocumentAdd}

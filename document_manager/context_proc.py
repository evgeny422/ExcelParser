from document_manager.forms import DocumentUpdateForm


def formDocUpdate(request):
    return {"formDocUpdate": DocumentUpdateForm}

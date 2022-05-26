from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput

from document_manager.models import Document


class DocumentUpdateForm(ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'password', 'uploaded_file',)
        widgets = {'password': PasswordInput}

    def clean_password(self):
        password = self.cleaned_data['password']

        if self.instance.password != password:
            raise ValidationError('Неверный пароль')

        return password

    def clean_uploaded_file(self):
        if not self.cleaned_data['uploaded_file']:
            raise ValidationError('Передайте файл')
        return self.cleaned_data['uploaded_file']

    def save(self, commit=True):
        self.instance.uploaded_file = self.cleaned_data['uploaded_file']
        self.instance.title = self.cleaned_data['title']
        self.instance.save()

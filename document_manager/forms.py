from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput, CharField

from document_manager.models import Document


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'password', 'uploaded_file', 'event')
        widgets = {'password': PasswordInput, }


class DocumentUpdateForm(ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'password', 'uploaded_file', 'event')
        widgets = {
            'password': PasswordInput,
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        if self.instance and self.instance.password != password:
            raise ValidationError('Неверный пароль')

        return password

    def save(self, commit=True):
        if self.instance:
            self.instance.uploaded_file = self.cleaned_data['uploaded_file']
            self.instance.title = self.cleaned_data['title']
            self.instance.event = self.cleaned_data['event']
            self.instance.save()
            return self.instance
        return super(DocumentUpdateForm, self).save(commit=True)

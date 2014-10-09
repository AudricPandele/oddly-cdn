from django import forms

class FileHandlerForm(forms.Form):
    uploaded_file = forms.FileField()

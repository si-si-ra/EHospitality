from django import forms
from .models import LoginTable


class LoginTableForm(forms.ModelForm):
        class Meta:
            model = LoginTable
            fields = ['type']
   


from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = (
      'username',
      'first_name',
      'last_name',
      'email',
      )
    widgets = {
      'username': forms.TextInput(attrs={'class' : 'form-control'}),
      'first_name': forms.TextInput(attrs={'class' : 'form-control'}),
      'last_name': forms.TextInput(attrs={'class' : 'form-control'}),
      'email': forms.TextInput(attrs={'class' : 'form-control', 'type':'email'}),

    }
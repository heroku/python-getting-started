from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
  class Meta:
    model = Person
    fields = (
      'bio',
      'picture',
      )
    widgets = {
      'bio': forms.Textarea(attrs={'class' : 'form-control'}),
    }
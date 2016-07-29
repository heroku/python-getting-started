from django import forms
from .models import Gig

class GigForm(forms.ModelForm):
	class Meta:
		model = Gig
		fields = ('title', 'description')
		widgets = {
			'description': forms.Textarea(attrs={'class' : 'form-control'}),
			'title': forms.TextInput(attrs={'class' : 'form-control'})
		}
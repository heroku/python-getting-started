from django import forms
from .models import Gig

class GigForm(forms.ModelForm):
	class Meta:
		model = Gig
		fields = ('title', 'description')
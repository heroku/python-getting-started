from django import forms
from django.contrib.auth.models import User


class OrgSignUp(forms.Form):
    organization_name = forms.CharField(label='Organization Name', max_length=255,
                                        widget=forms.TextInput(attrs={'placeholder': 'Enter organization name'}))
    email = forms.EmailField(label='Email', max_length=255,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter email address'}))
    password = forms.CharField(label='Password', max_length=255,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    repeat_password = forms.CharField(label='Repeat Password', max_length=255,
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    def clean(self):
        cleaned_data = super(OrgSignUp, self).clean()
        try:
            _user = User.objects.get(email=cleaned_data.get('email'))
            raise forms.ValidationError('This email is already taken')
        except User.DoesNotExist:
            pass
        if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
            raise forms.ValidationError('Password doesn\'t match the confirmation')
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
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
        }


class OrgSignUpForm(forms.Form):
    organization_name = forms.CharField(label='Organization Name', max_length=255,
                                        widget=forms.TextInput(attrs={'placeholder': 'Enter organization name'}))
    email = forms.EmailField(label='Email', max_length=255,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter email address'}))
    password = forms.CharField(label='Password', max_length=255,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    repeat_password = forms.CharField(label='Repeat Password', max_length=255,
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    def clean(self):
        cleaned_data = super(OrgSignUpForm, self).clean()
        try:
            _user = User.objects.get(email=cleaned_data.get('email'))
            raise forms.ValidationError('This email is already taken')
        except User.DoesNotExist:
            pass
        if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
            raise forms.ValidationError('Password doesn\'t match the confirmation')


class UserSignUpForm(forms.Form):
    email = None
    password = forms.CharField(label='Password', max_length=255,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    repeat_password = forms.CharField(label='Repeat Password', max_length=255,
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    def set_email(self, email):
        self.email = email

    def clean(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
            raise forms.ValidationError('Password doesn\'t match the confirmation')
        try:
            _user = User.objects.get(email=self.email)
        except:
            _user = None
        if _user is not None:
            raise forms.ValidationError('This email is already taken')


class SettingsForm(forms.Form):
    user = None
    name = forms.CharField(label='Name', max_length=255, required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'Enter name'}))
    email = forms.EmailField(label='Email', max_length=255,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter email address'}))
    password = forms.CharField(label='Password', max_length=255, required=False,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    repeat_password = forms.CharField(label='Repeat Password', max_length=255, required=False,
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))
    userpic = forms.ImageField(label='Picture', required=False)


    def set_user(self, user):
        self.user = user

    def clean(self):
        cleaned_data = super(SettingsForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
            raise forms.ValidationError('Password doesn\'t match the confirmation')

        users = User.objects.filter(email=cleaned_data.get('email'))
        if len(users) > 0:
            if users[0].pk != self.user.pk:
                raise forms.ValidationError('This email is already taken')

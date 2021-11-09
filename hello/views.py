import requests
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting


from django import forms

class SuggestForm(forms.Form):
    color = forms.CharField(label='Farbe', max_length=100)
    describtion = forms.CharField(label='Beschreibung', max_length=100)


# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST': # TODO: this needs to be implemented correctly
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        context = {} # TODO: here I transport if I want to show suggest, wait or draw and with which values
        return render(request, "index.html", context)




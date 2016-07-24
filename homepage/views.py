import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Greeting

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/app')
	else:
		return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


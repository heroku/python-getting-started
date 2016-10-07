import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Greeting
from app.models import Lead


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/app')
    else:
        if request.method == "POST":
        	email=request.POST['email']
        	new_lead=Lead(email=email)
        	new_lead.save()
        	context={
        		'alert':email,
        	}

        	return render(request, 'index.html', context)
        else:
        	return render(request, 'index.html')


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

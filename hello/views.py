#import requests
import os
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

## Create your views here.
#def index(request):
#    return HttpResponse('Hello from Python!')
#    return render(request, 'index.html')
#def index(request):
#    r = requests.get('http://httpbin.org/status/418')
#    print(r.text)
#    return HttpResponse('<pre>' + r.text + '</pre>')
def index(request):
    times = int(os.environ.get('TIMES',3))
    return HttpResponse('Hello! ' * times)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


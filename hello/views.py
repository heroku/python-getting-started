#import requests
import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Greeting

## Create your views here.
#def index(request):
#    return HttpResponse('Hello from Python!')
#    return render(request, 'index.html')
#def index(request):
#    r = requests.get('http://httpbin.org/status/418')
#    print(r.text)
#    return HttpResponse('<pre>' + r.text + '</pre>')
#def index(request):
#    times = int(os.environ.get('TIMES',3))
#    return HttpResponse('Hello! ' * times)

def index(request):
    headers = {"Content-Type" : "application/json"}
    obj = {
        "speech": "Barack Hussein Obama II was the 44th and current President of the United States.",
        "displayText": "Barack Hussein Obama II was the 44th and current President of the United States, and the first African American to hold the office. Born in Honolulu, Hawaii, Obama is a graduate of Columbia University   and Harvard Law School, where ",
        "data": {"kik": {}},
        "contextOut": [{"name":"weather", "lifespan":2, "parameters":{"city":"Rome"}}],
        "source": "DuckDuckGo"
    }
    return JsonResponse(obj)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


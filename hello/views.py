from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import requests

# Create your views here.
def index(request):
    r = requests.get('https://httpbin.org/status/418')
    print(r.text)

    d = '{"richContent":[[{"type":"description","title":"Description title","text":["This is text line 1.","This is text line 2."]}]]}'
    return HttpResponse('<pre>' + d + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

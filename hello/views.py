from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Greeting
import requests

# Create your views here.
@csrf_exempt
def index(request):
    #r = requests.get('https://httpbin.org/status/418')
    #print(r.text)

    d = '{"fulfillmentMessages": [{"card": {"title": "card title","subtitle": "card text","imageUri": "https://example.com/images/example.png","buttons": [{"text": "button text","postback": "https://example.com/path/for/end-user/to/follow"}]}}]}'
    return HttpResponse('<pre>' + d + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

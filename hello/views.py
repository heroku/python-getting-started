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

    d = '{"richContent":[[{"type":"info","title":"Exit to Dialogflow","subtitle":"Dialogflow is Googles natural language understanding tool for ...","image":{"src":{"rawUrl":"https://i.ytimg.com/vi/yT58gTXdQb8/maxres3.jpg"}},"actionLink":"https://www.youtube.com/watch?v=yT58gTXdQb8"}]]}'
    return HttpResponse(d)




def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

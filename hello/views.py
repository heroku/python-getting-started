from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import time

from .models import Greeting

@xframe_options_exempt
def index(request):
    # return HttpResponse('Hello from Python!')
    time.sleep(1)
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

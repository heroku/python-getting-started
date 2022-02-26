from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    context = {
        "firstDistrict": "Gary Anderson",
        "secondDistrict": "Mike Mayou",
        "thirdDistrict": "Roz Randorf",
        "fourthDistrict": "Renee Van Nett",
        "fifthDistrict": "Janet Kennedy",
        "councilor1": "Arik Forsman",
        "councilor2": "Azrin Awal",
        "councilor3": "Derek Medved",
        "councilor4": "Terese Tomanek"    
    }
    return render(request, "index.html", context)

def city(request):
    
    return render(request, "city.html")

def County(request):
    
    return render(request, "county.html")

def state(request):
    
    return render(request, "state.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

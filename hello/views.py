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

    d = """{
        "payload": {
            "google": {
            "expectUserResponse": true,
            "richResponse": {
                "items": [
                {
                    "simpleResponse": {
                    "textToSpeech": "This is a Basic Card:"
                    }
                },
                {
                    "basicCard": {
                    "title": "Card Title",
                    "image": {
                        "url": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                        "accessibilityText": "Google Logo"
                    },
                    "buttons": [
                        {
                        "title": "Button Title",
                        "openUrlAction": {
                            "url": "https://www.google.com"
                        }
                        }
                    ],
                    "imageDisplayOptions": "WHITE"
                    }
                }
                ]
            }
            }
        }
        }"""
    return HttpResponse(d)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

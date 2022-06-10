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
    #return HttpResponse('<pre>' + d + '</pre>')
    req = request.get_json()

    tag = req["fulfillmentInfo"]["tag"]

    if tag == "Default Welcome Intent":
        # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
        # Please see https://googleapis.dev/python/dialogflow/latest/dialogflow_v2/types.html?highlight=webhookresponse#google.cloud.dialogflow_v2.types.WebhookResponse for an overview
        res = {
            "fulfillment_response": {
                "messages": [{"text": {"text": ["Hi from a GCF Webhook"]}}]
            }
        }
    elif tag == "get-name":
        res = {
            "fulfillment_response": {
                "messages": [{"text": {"text": ["My name is Phlowhook"]}}]
            }
        }
    else:
        res = {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [
                                f"There are no fulfillment responses defined for {tag} tag"
                            ]
                        }
                    }
                ]
            }
        }

    # Returns json
    return res



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

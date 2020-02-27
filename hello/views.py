import os
import requests
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting


# Create your views here.
def index(request):
    times = int(os.environ.get('TIMES', 3))
    return HttpResponse('''<script type="text/javascript" async src="https://d335luupugsy2.cloudfront.net/js/loader-scripts/40552c01-2431-44a2-9bb6-ead4fbb70f44-loader.js" ></script>
<!-- Start of HubSpot Embed Code -->
<script type="text/javascript" id="hs-script-loader" async defer src="//js.hs-scripts.com/7226535.js"></script>
<!-- End of HubSpot Embed Code -->
<h1>Hello!</h1>''')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

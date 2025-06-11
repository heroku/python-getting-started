from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Greeting

# Create your views here.


def index(request):
    return render(request, "index.html")

@csrf_exempt
def execute_script(request):
    print("MADE IT TO THE SCRIPT EXECUTION VIEW")
    """
    A view to execute a script from the request body.
    This is a placeholder for any script execution logic you want to implement.
    """
    if request.method == "POST":
        # Here you would execute the script, but be careful with security implications!
        # For demonstration purposes, we just return the script.
        return render(request, "script_result.html", {"result": "ooga booga dooga"})
    else:
        return render(request, "script_result.html", {"result": "Please send a POST request with a script."})


def db(request):
    # If you encounter errors visiting the `/db/` page on the example app, check that:
    #
    # When running the app on Heroku:
    #   1. You have added the Postgres database to your app.
    #   2. You have uncommented the `psycopg` dependency in `requirements.txt`, and the `release`
    #      process entry in `Procfile`, git committed your changes and re-deployed the app.
    #
    # When running the app locally:
    #   1. You have run `./manage.py migrate` to create the `hello_greeting` database table.

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

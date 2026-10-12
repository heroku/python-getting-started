from django.shortcuts import render

from .models import Greeting

# Create your views here.


def index(request):
    return render(request, "index.html")


def db(request):
    # If you encounter errors visiting the `/db/` page on the example app, check that:
    #
    # When running the app on Heroku:
    #   1. You have added the Heroku Postgres database add-on to your app.
    #   2. You have added the `psycopg` dependency using `uv add "psycopg[binary]"`, uncommented
    #      the `release` process entry in `Procfile`, git committed your changes and re-deployed
    #      the app.
    #
    # When running the app locally:
    #   1. You have run `uv run manage.py migrate` to create the `hello_greeting` database table.

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person
from teams.models import Team

@login_required
def index(request):
    people = Person.objects.all()
    teams = Team.objects.all()
    context = {
        'people':people,
        'teams':teams,
    }
    return render(request, 'app/home.html', context)

def login_user(request):
    #logout(request)
    username = password = ''
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/app')
            else:
                return HttpResponse("Please check your username or password and try again.")
        else:
            return HttpResponse("Please check your username or password and try again.")

def login_view(request):
    try:
        next = request.GET['next']
        context = {'next':next }
    except:
        context = {}

    return render(request, 'app/login.html',context)

def signup(request):
    return render(request, 'app/signup.html')
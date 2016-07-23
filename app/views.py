from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person

@login_required
def index(request):
    people = Person.objects.all()
    context = {
        'people':people,
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
    return HttpResponse("You're authenticated.")

def login_view(request):
    try:
        next = request.GET['next']
        context = {'next':next }
    except:
        context = {}

    return render(request, 'app/login.html',context)

def signup(request):
    return render(request, 'app/signup.html')
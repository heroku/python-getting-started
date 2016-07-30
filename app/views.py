from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person
from .forms import UserForm
from django.contrib.auth.models import User
from django.shortcuts import redirect

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

def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form=UserForm(request.POST, instance=user)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            return redirect('index')
    else:
            form=UserForm(instance=user)
    return render(request, 'app/profile_edit.html', {'form': form})

def signup(request):
    return render(request, 'app/signup.html')
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person
from .models import Alert
from .forms import UserForm
from people.forms import PersonForm
from django.contrib.auth.models import User
from django.shortcuts import redirect

@login_required
def index(request):
    try:
        alert=get_object_or_404(Alert, name=request.GET['alert'])
        context = {
            'alert': alert,
        }
        return render(request, 'app/home.html', context)
    except:
        return render(request, 'app/home.html')

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
    person = Person.objects.get(profile=user)
    if request.method == "POST":
        form=UserForm(request.POST, instance=user)
        if form.is_valid():
            person_form=PersonForm(request.POST, instance=person)
            if person_form.is_valid():
                user=form.save(commit=False)
                person=person_form.save(commit=False)
                user.save()
                person.save()
                return redirect('/app/?alert=profile_update')
    else:
            form=UserForm(instance=user)
            person_form=PersonForm(instance=person)
    return render(request, 'app/profile_edit.html', {'form': form, 'person_form': person_form})

def signup(request):
    return render(request, 'app/signup.html')
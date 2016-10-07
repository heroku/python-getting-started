from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .models import Alert
from teams.models import Team
from teams.forms import OrgSignUp


@login_required
def index(request):
    teams = Team.objects.all()
    myteams = [member.team for member in request.user.member_set.all()]
    otherteams = [team for team in teams if team not in myteams]
    context = {
        'teams': teams,
        'myteams': myteams,
        'otherteams': otherteams,
    }
    return render(request, 'app/home.html', context)


def login_user(request):
    # logout(request)
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
        context = {'next': next}
    except:
        context = {}

    return render(request, 'app/login.html', context)


def edit_profile(request):
    # user = request.user
    # person = Person.objects.get(profile=user)
    # if request.method == "POST":
    #     form = UserForm(request.POST, instance=user)
    #     if form.is_valid():
    #         person_form = PersonForm(request.POST, request.FILES, instance=person)
    #         if person_form.is_valid():
    #             user = form.save(commit=False)
    #             person = person_form.save(commit=False)
    #             user.save()
    #             person.save()
    #             return redirect('/app/?alert=profile_update')
    # else:
    #     form = UserForm(instance=user)
    #     person_form = PersonForm(instance=person)
    return render(request, 'app/profile_edit.html', locals())


def signup(request):
    form = OrgSignUp()
    if request.method == 'POST':
        form = OrgSignUp(request.POST)
        if form.is_valid():
            print 'user created'
        
    return render(request, 'app/signup.html', locals())

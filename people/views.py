from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person
from gigs.models import Gig, Team

@login_required
def index(request):
    people = Person.objects.all()
    context = {
        'people':people,
    }
    return render(request, 'people/home.html', context)

@login_required
def profile_view(request, profile_id):
    person = Person.objects.get(pk=profile_id)
    user = person.profile

    teams = Team.objects.filter(person=user).filter(approved=True)

    context = {
		'person': person,
        'user': user,
        'teams': teams,
		}
	
    return render(request, 'people/profile.html', context)

@login_required
def timekittest(request):
    return render(request, 'people/timekit-test.html')
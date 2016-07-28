from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person

@login_required
def index(request):
    return render(request, 'gigs/home.html')

def gig_detail(request):
	return render(request, 'gigs/gig_detail.html')
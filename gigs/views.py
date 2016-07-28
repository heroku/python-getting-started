from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person
from gigs.models import Gig

@login_required
def index(request):
	gigs = Gig.objects.all()
	context = {
		'gigs':gigs,
	}
	return render(request, 'gigs/home.html', context)

def gig_detail(request, gig_id):
	gig = Gig.objects.get(pk=gig_id)
	context = {
		'gig':gig,
	}
	return render(request, 'gigs/gig_detail.html', context)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person
from gigs.models import Gig
from .forms import GigForm
from django.shortcuts import redirect

@login_required
def index(request):
	gigs = Gig.objects.all().order_by('-modified')
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

def new_gig(request):
	if request.method == "POST":
		form = GigForm(request.POST)
		if form.is_valid():
			
			post = form.save(commit=False)
			post.owner = request.user

			post.save()
			return redirect('/gigs')
	else:
		form = GigForm()
		return render(request, 'gigs/gig_edit.html', {'form': form})
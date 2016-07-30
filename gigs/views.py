from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
	try:
		gig = Gig.objects.get(pk=gig_id)
		context = {
			'gig':gig,
		}
		return render(request, 'gigs/gig_detail.html', context)
	except:
		return redirect('index')

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

def edit_gig(request, pk):
	gig = get_object_or_404(Gig, pk=pk)

	#Need to make sure those who are not post owners cannot edit
	if request.user == gig.owner:
		if request.method == "POST":
			form=GigForm(request.POST, instance=gig)
			if form.is_valid():
				gig=form.save(commit=False)
				gig.owner=request.user
				gig.save()
				return redirect('gig_detail', gig_id=gig.pk)
		else:
				form=GigForm(instance=gig)
				context = {
					'form':form,
					'gig':gig,
				}
		return render(request, 'gigs/gig_edit.html', context)
	else:
		return redirect('gig_detail', gig_id=gig.pk)
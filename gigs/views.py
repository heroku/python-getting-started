from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from people.models import Person
from gigs.models import Gig, Role, Team
from .forms import GigForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def index(request):
	#need to implement pagination into the template at some point

	gig_list = Gig.objects.all().order_by('-modified')
	paginator = Paginator(gig_list, 100) #show 100 gigs per page

	page = request.GET.get('page')
	try:
		gigs=paginator.page(page)
	except PageNotAnInteger:
		#if page not integer deliver first page
		gigs=paginator.page(1)
	except EmptyPage:
		#page out of range to go to last page
		gigs=paginator.page(paginator.num_pages)

	context = {
		'gigs':gigs,
	}
	return render(request, 'gigs/home.html', context)

def gig_detail(request, gig_id):
	try:
		gig = Gig.objects.get(pk=gig_id)
		role = Role.objects.get(role='admin')
		gig_admin = Team.objects.filter(role=role).filter(gig=gig)
		
		user_role = Team.objects.filter(gig=gig).filter(person=request.user)
		length=len(user_role)-1
		admin = user_role[length].approved

		try:
			membership = Team.objects.filter(person=request.user).filter(gig=gig)
			membership_status = membership[len(membership)-1].approved
		except:
			membership_status = 'Request to join'

		context = {
			'gig':gig,
			'gig_admin': gig_admin,
			'admin': admin,
			'membership_status': membership_status,
		}
		return render(request, 'gigs/gig_detail.html', context)
	except:
		return redirect('index')

def new_gig(request):
	if request.method == "POST":
		form = GigForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			gig_id = post.pk
			new_gig = Gig.objects.get(pk=post.pk)

			user = request.user
			role = Role.objects.get(role='admin')
			new_team_membership = Team.objects.create(person=user, gig=new_gig, role=role, approved=True)
			#return HttpResponse(post.pk)
			return redirect('gig_detail', gig_id)
	else:
		form = GigForm()
		return render(request, 'gigs/gig_edit.html', {'form': form})

def team_request(request, gig_id):
	person=request.user
	gig=Gig.objects.get(pk=gig_id)
	role=Role.objects.get(role='member')

	new_team_membership = Team.objects.create(person=person, gig=gig, role=role)

	return redirect('gig_detail', gig_id)

def edit_gig(request, pk):
	gig = get_object_or_404(Gig, pk=pk)
	user_role = Team.objects.filter(gig=gig).filter(person=request.user)
	length=len(user_role)-1
	admin = user_role[length].approved
	
	#Need to make sure those who are not post owners cannot edit
	if admin:
		if request.method == "POST":
			form=GigForm(request.POST, instance=gig)
			if form.is_valid():
				gig=form.save(commit=False)
				#gig.admin=request.user
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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from teams.models import Team


@login_required
def index(request):
    context = {}
    return render(request, 'teams/index.html', context)

@login_required
def team_detail(request, team_id):
	team = Team.objects.get(pk=team_id)
	context = {
		'team':team,
	}
	return render(request, 'teams/team_detail.html', context)

@login_required
def team_delete(request, team_id):
	team = Team.objects.get(pk=team_id)
	if request.user == team.owner:
		team.delete()
		return redirect('/app')
	else:
		return redirect('/app')

@login_required
def create_new_team(request):
	title=request.POST.get('title')
	description=request.POST['description']
	team_image = request.FILES['team_image']

	new_team=Team(title=title, description=description, owner=request.user, image=team_image)

	new_team.save()

	return redirect('/app/')
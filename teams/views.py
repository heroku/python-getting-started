from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from teams.models import Team, Role, Member


@login_required
def index(request):
    context = {}
    return render(request, 'teams/index.html', context)


@login_required
def team_detail(request, team_id):
    """
        TODOs:
        0) check if current user has access to this team
        1) fallback to 404 on wrong ids
    """
    team = Team.objects.get(pk=team_id)
    context = {
        'team': team,
    }
    return render(request, 'teams/team_detail.html', context)


@login_required
def team_delete(request, team_id):
    # TODO: delete actions shouldn't be available as GET requests to prevent CSRF attacks
    team = Team.objects.get(pk=team_id)
    if request.user in team.owners:
        team.delete()
        return redirect('/app')
    else:
        return redirect('/app')


@login_required
def create_new_team(request):
    # TODO: additional validation required
    title = request.POST.get('title')
    description = request.POST['description']
    team_image = request.FILES['team_image']

    team = Team(title=title, description=description, image=team_image)
    team.save()

    Member(user=request.user, is_owner=True, team=team).save()

    return redirect('/app/')

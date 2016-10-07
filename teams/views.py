from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from teams.models import Team, Role, Member

import datetime


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
    description = request.POST.get('description')
    team_image = request.FILES['team_image']

    team = Team(title=title, description=description, image=team_image)
    team.save()

    Member(user=request.user, is_owner=True, team=team).save()

    return redirect('/app/')


@login_required
def roles(request, team_id):
    # TODO: validation missing
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        return create_role(request, team)

    raise Http404


def create_role(request, team):
    title = request.POST.get('role_title')
    description = request.POST.get('role_description')
    start_date = datetime.datetime.strptime(request.POST.get('start_date'), '%m-%d-%Y %H:%M')
    end_date = datetime.datetime.strptime(request.POST.get('start_date'), '%m-%d-%Y %H:%M')
    Role(team=team, title=title, description=description, start_date=start_date, end_date=end_date).save()
    return redirect(reverse('team_detail', kwargs={'team_id': team.pk}))
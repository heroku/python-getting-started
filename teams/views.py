from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from teams.models import Team, Role, Member, Invite
from django.contrib.auth.models import User

from datetime import datetime, timedelta


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
    # ToDo - This should fetch members who belong to team's organization, once organization is implemented
    nonmembers = [user for user in User.objects.all() if user not in team.members]
    invitees = [invite.invitee for invite in request.user.invites.all()]
    context = {
        'team': team,
        'nonmembers': nonmembers,
        'invitees': invitees
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

@login_required
def invite_people(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        return _invite_people(request, team)

    raise Http404

def _invite_people(request, team):
    invitees = [User.objects.get(pk=invitee_id) for invitee_id in request.POST.get('invitees').split(",")]
    for invitee in invitees:
        invitation = Invite(team=team, inviter=request.user, invitee=invitee, status='created', expired_at=datetime.now()+timedelta(days=7), read=False)
        invitation.save()

    return HttpResponse(status=200)

@login_required
def invite_accept(request, invite_id):
    try: 
        invite = Invite.objects.get(pk=invite_id)
        invite.status = 'accepted'
        invite.save()
        member = Member(is_owner=False, team_id=invite.team.pk, user_id=request.user.pk)
        member.save()
    except Invite.DoesNotExist:
        raise Http404

    return HttpResponse(status=200)    

@login_required
def invite_reject(request, invite_id):
    try: 
        invite = Invite.objects.get(pk=invite_id)
        invite.status = 'rejected'
        invite.save()
    except Invite.DoesNotExist:
        raise Http404

    return HttpResponse(status=200)   
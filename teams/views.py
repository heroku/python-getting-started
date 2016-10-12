from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from teams.models import Team, Role, Member, Invite, JoinRequest
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
    invitees = [invite.invitee for invite in request.user.invites.all().filter(status="created")]
    joinrequest = request.user.team_join_requests.all().filter(team__id=team_id).filter(status="created")

    if request.user in [user for user in team.members]:
        context = {
            'team': team,
            'nonmembers': nonmembers,
            'invitees': invitees
        }
        return render(request, 'teams/team_detail.html', context)
    else:
        context = {
            'team': team,
            'join_requested': len(joinrequest) > 0,
            'members_count': len(team.members)
        }
        return render(request, 'teams/team_detail_nonmember.html', context)


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
@csrf_exempt
def roles(request, team_id):
    # TODO: validation missing
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        return createupdate_role(request, team)
    elif request.method == 'DELETE':
        return delete_role(request, team)
    raise Http404

def createupdate_role(request, team):
    role = Role()
    role_id = request.POST.get('id')
    if role_id is not None:
        role = get_object_or_404(Role, pk=role_id, team=team)
    role.team = team
    role.title = request.POST.get('role_title')
    role.description = request.POST.get('role_description')
    role.start_date = datetime.strptime(request.POST.get('start_date'), '%m-%d-%Y %H:%M')
    role.end_date = datetime.strptime(request.POST.get('end_date'), '%m-%d-%Y %H:%M')
    role.save()
    if request.is_ajax():
        return HttpResponse('{}')
    return redirect(reverse('team_detail', kwargs={'team_id': team.pk}))

def delete_role(request, team):
    role = get_object_or_404(Role, pk=request.GET.get('role_id'))
    role.delete()
    return HttpResponse('{}')

@login_required
def invite_people(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        return _invite_people(request, team)

    raise Http404

def _invite_people(request, team):
    # TODO: optimize it
    # we can do `invitees = User.objects.filter(pk__in=request.POST.get('invitees').split(","))`
    # single db query usually works faster due to internal db caching system
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

@login_required
def request_join(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        return _request_join(request, team)

    raise Http404

def _request_join(request, team):
    join_request = JoinRequest(team=team, requester=request.user, status='created', expired_at=datetime.now()+timedelta(days=7), read=False)
    join_request.save()

    return HttpResponse(status=200)

@login_required
def joinrequest_accept(request, request_id):
    try: 
        joinrequest = JoinRequest.objects.get(pk=request_id)
        joinrequest.status = 'accepted'
        joinrequest.save()
        member = Member(is_owner=False, team_id=joinrequest.team.pk, user_id=joinrequest.requester.pk)
        member.save()
    except Invite.DoesNotExist:
        raise Http404

    return HttpResponse(status=200)    

@login_required
def joinrequest_reject(request, request_id):
    try: 
        joinrequest = JoinRequest.objects.get(pk=request_id)
        joinrequest.status = 'rejected'
        joinrequest.save()
    except Invite.DoesNotExist:
        raise Http404

    return HttpResponse(status=200) 
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt # TODO: switch to valid protection instead of csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic import View

from app.models import Organization, OrganizationMember, OrganizationInvitation
from teams.models import Team, Role, Member

import datetime
import json


"""
    TODO:
    integrate @check_auth decorator
"""

def json_response(data={}, status=200):
    return JsonResponse(data, status=status)


def index(request):
    """
        A simple API backend which allows to check if it's alive
    """
    return json_response()



"""
    Settings page / Organization methods
"""

def get_membership(org_id, user_id):
    try:
        return OrganizationMember.objects.get(organization_id=org_id, user_id=user_id)
    except OrganizationMember.DoesNotExist:
        return None

def get_organization(org_id):
    try:
        return Organization.objects.get(pk=org_id)
    except Organization.DoesNotExist:
        return None

@csrf_exempt
def organization_switch_admin_status(request, org_id, user_id):
    # TODO: check permissions & request method
    membership = get_membership(org_id, user_id)
    if not membership:
        return json_response(status=404)
    membership.is_owner = not membership.is_owner
    membership.save()
    return json_response({'button_text': 'Revoke admin' if membership.is_owner else 'Make admin'}, status=201)

@csrf_exempt
def organization_remove_member(request, org_id, user_id):
    # TODO: check permissions & request method
    membership = get_membership(org_id, user_id)
    if not membership:
        return json_response(status=404)
    membership.delete()
    return json_response(status=201)

@csrf_exempt
def organization_invite(request, org_id):
    # TODO: check permissions & request method
    organization = get_organization(org_id)
    if not organization:
        return json_response(status=404)

    email = request.POST.get('email')
    if not email:
        return json_response(status=400)

    try:
        user = User.objects.get(email='email')
    except User.DoesNotExist:
        user = None

    if user is not None:
        try:
            membership = OrganizationMember.objects.get(user=user, organization=organization)
        except OrganizationMember.DoesNotExist:
            membership = None
        if membership is None and len(OrganizationMember.objects.filter(user=user, is_owner=True)) == 0:
            OrganizationMember(user=user, organization=organization).save()
    else:
        inv = OrganizationInvitation()
        inv.organization = organization
        inv.email = email
        inv.save()
        link = request.build_absolute_uri(reverse('join-organization', args=[inv.token]))
        send_mail('Organization invitation', settings.ORGANIZATION_INVITATION_EMAIL % (organization.name, link,),
                  'support@teamedup.com', [email, ])

    return json_response({'email': email})


class TeamRolesView(View):
    """
    TODO: validate user!
    """
    def get(self, request, team_id):
        team = Team.objects.get(pk=team_id)
        roles = [role.to_dict() for role in Role.objects.filter(team=team)]
        return json_response({'entries': roles})

    def post(self, request, team_id):
        team = Team.objects.get(pk=team_id)
        data = json.loads(request.body)

        role = Role()
        role_id = data.get('id')
        if role_id is not None:
            role = Role.objects.get(pk=role_id)
        role.team = team
        role.title = data.get('title')
        role.description = data.get('description')
        role.start_date = datetime.datetime.strptime(data.get('start_date'), '%m-%d-%Y %H:%M')
        role.end_date = datetime.datetime.strptime(data.get('end_date'), '%m-%d-%Y %H:%M')
        role.save()

        return json_response(role.to_dict())

    def delete(self, request, team_id):
        role_id = request.GET.get('role_id')
        role = Role.objects.get(pk=role_id)
        role.delete()
        return json_response()


class TeamView(View):
    """
    TODO: validate user!
    """
    def get(self, request, team_id=None):
        if team_id is not None:
            return self.get_single(request, team_id)
        return json_response()

    def get_single(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return json_response(status=404)
        return json_response(team.to_dict())
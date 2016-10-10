from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt # TODO: switch to valid protection instead of csrf_exempt

from app.models import Organization, OrganizationMember

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
    email = request.POST.get('email')
    if not email:
        return json_response(status=400)
    """
        TODO: Build behavior for the invitations
    """
    return json_response({'email': email})
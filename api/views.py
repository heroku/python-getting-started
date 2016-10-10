from django.http import JsonResponse


def json_response(data={}, status=200):
    return JsonResponse(data, status=status)


def index(request):
    return json_response()



"""
    Settings page / Organization methods
"""

def organization_switch_admin_status(request, org_id, user_id):
    return json_response()


def organization_remove_member(request, org_id, user_id):
    return json_response()
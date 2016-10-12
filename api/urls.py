from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^$', views.index, name='api-index'),
    url(r'^organization/(?P<org_id>\d+)/switch-admin-status/(?P<user_id>\d+)/$',
        views.organization_switch_admin_status, name='organization-switch-admin-status'),
    url(r'^organization/(?P<org_id>\d+)/remove-member/(?P<user_id>\d+)/$',
        views.organization_remove_member, name='organization-remove-member'),
    url(r'^organization/(?P<org_id>\d+)/invite/$', views.organization_invite, name='organization-invite'),
]
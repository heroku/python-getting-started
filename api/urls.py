from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^$', views.index, name='api-index'),
    url(r'^organization/(?P<org_id>[0-9]+)/switch-admin-status/(?P<user_id>[0-9]+)/^',
        views.organization_switch_admin_status, name='organization-switch-admin-status'),
    url(r'^organization/(?P<org_id>[0-9]+)/remove-member/(?P<user_id>[0-9]+)/^',
        views.organization_remove_member, name='organization-remove-member'),

]

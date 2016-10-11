from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<team_id>[0-9]+)/$', views.team_detail, name='team_detail'),
    url(r'^detail/(?P<team_id>[0-9]+)/delete/$', views.team_delete, name='team_delete'),
    url(r'^create_new_team/$', views.create_new_team, name='create_new_team'),
    url(r'^detail/(?P<team_id>[0-9]+)/roles/$', views.roles, name='team_roles'),
    url(r'^detail/(?P<team_id>[0-9]+)/invitepeople/$', views.invite_people, name='team_invite_people'),
    url(r'^invites/(?P<invite_id>[0-9]+)/accept/$', views.invite_accept, name='invite_accept'),
    url(r'^invites/(?P<invite_id>[0-9]+)/reject/$', views.invite_reject, name='invite_reject'),
    url(r'^detail/(?P<team_id>[0-9]+)/requestjoin/$', views.request_join, name='team_request_join'),
    url(r'^joinrequests/(?P<request_id>[0-9]+)/accept/$', views.joinrequest_accept, name='joinrequest_accept'),
    url(r'^joinrequests/(?P<request_id>[0-9]+)/reject/$', views.joinrequest_reject, name='joinrequest_reject'),
]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<team_id>[0-9]+)/$', views.team_detail, name='team_detail'),
    url(r'^detail/(?P<team_id>[0-9]+)/delete/$', views.team_delete, name='team_delete'),
    url(r'^create_new_team/$', views.create_new_team, name='create_new_team'),
]
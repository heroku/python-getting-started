from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile_view, name='profile view'),
	url(r'^timekit/', views.timekittest, name='timekit test'),

]
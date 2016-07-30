from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^profile/$', views.profile_view, name='profile_view'),
    url(r'^signup$', views.signup, name='signup'),
]
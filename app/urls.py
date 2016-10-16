from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^settings/$', views.edit_settings, name='settings'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signout/$', views.sign_out, name='sign-out'),
    url(r'^activate/(?P<token>\w+)/$', views.activate_account, name='activate-account'),
    url(r'^join/(?P<token>\w+)/$', views.join_organization, name='join-organization'),
	url(r'^getnotifications$', views.getnotifications, name='getnotifications'),
	url(r'^notifications$', views.notifications, name='notifications'),
	url(r'^people$', views.searchpeople, name='search-people'),
    url(r'^member/(?P<user_id>\d+)/$', views.user_page, name='user-page'),
]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'), # TODO: url and view names are confusing
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^settings/$', views.edit_settings, name='settings'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signout/$', views.sign_out, name='sign-out'),
    url(r'^activate/(?P<token>\w+)/$', views.activate_account, name='activate-account'),
	url(r'^notifications$', views.notifications, name='notifications'),
]

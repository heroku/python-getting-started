from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^detail/(?P<gig_id>[0-9]+)', views.gig_detail, name='gig detail'),
	url(r'^new_gig/$', views.new_gig, name='new gig'),
]
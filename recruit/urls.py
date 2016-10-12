from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^newsearch/', views.new_search, name='new search'),
    url(r'^campaigndetail/', views.campaign_detail, name='campaign detail'),

]

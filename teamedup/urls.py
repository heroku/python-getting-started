from django.conf.urls import include, url

from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

import homepage.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^app/', include('app.urls')),
    url(r'^$', homepage.views.index, name='index'),
    url(r'^db', homepage.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
]

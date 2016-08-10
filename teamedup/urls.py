from django.conf.urls import include, url
from django.conf import settings
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
    url(r'^message/', include('message.urls')),
    url(r'^people/', include('people.urls')),
    url(r'^gigs/', include('gigs.urls')),
    url(r'^recruit/', include('recruit.urls')),
    url(r'^$', homepage.views.index, name='index'),
    url(r'^db', homepage.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
]

from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    path('', hello.views.index, name='index'),
    path('db/', hello.views.db, name='db'),
    path('admin/', admin.site.urls),
]

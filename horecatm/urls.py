from django.conf.urls import include, url
from django.urls import path

from horecatm.views import UserView

from django.contrib import admin
admin.autodiscover()


# Examples:
# url(r'^$', 'horecatm.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/<int:pk>/', UserView.as_view(), name='user-detail'),
]

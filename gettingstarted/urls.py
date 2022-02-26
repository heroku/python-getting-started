from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    
    path("city/", hello.views.city, name="city"),
    path("City/", hello.views.city, name="City"),
    
    path('county/', hello.views.county, name="county"),
    path('County/', hello.views.county, name="County"),

    path("state/", hello.views.state, name="state"),
    path("State/", hello.views.state, name="State"),



    
    path("admin/", admin.site.urls),
]

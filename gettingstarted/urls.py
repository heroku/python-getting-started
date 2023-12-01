"""
URL configuration for gettingstarted project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.conf import settings

import hello.views

def error(request):
    if settings.SHOULD_ERROR:
        division_by_zero = 1 / 0
    else:
        return render(request, "fixed.html")

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("error/", error, name="error"),
    path("db/", hello.views.db, name="db"),
    # Uncomment this and the entry in `INSTALLED_APPS` if you wish to use the Django admin feature:
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/
    # path("admin/", admin.site.urls),
]

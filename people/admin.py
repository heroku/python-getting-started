from django.contrib import admin
from django.db import models
from .models import Person, Membership

# Register your models here.

admin.site.register(Person)
admin.site.register(Membership)
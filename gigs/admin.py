from django.contrib import admin
from django.db import models
from .models import Gig, Role, Team

# Register your models here.
admin.site.register(Gig)
admin.site.register(Role)
admin.site.register(Team)

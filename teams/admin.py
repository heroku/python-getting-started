from django.contrib import admin
from django.db import models
from .models import Team, Role, Member, Invite

# Register your models here.
admin.site.register(Team)
admin.site.register(Role)
admin.site.register(Member)
admin.site.register(Invite)

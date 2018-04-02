"""Setup admin panel content."""
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from horecatm.models import User


class UserAdmin(BaseUserAdmin):
    """Extending HoReKa user admin model with Django base."""


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

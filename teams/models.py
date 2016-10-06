from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    # Image upload is working for S3 bucket, but not for local environment (local development relies on connection to S3 at the moment)
    image = models.ImageField('img', upload_to='media/images/', default='img/dashboard_template_image.png')
    # created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) # TODO: add created_at field

    @property
    def owners(self):
        return [member.user for member in self.member_set.filter(is_owner=True)]

    def __str__(self):
        return self.title


class Role(models.Model):
    title = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    start_date = models.DateTimeField(default=None, blank=True, null=True)
    end_date = models.DateTimeField(default=None, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Member(models.Model):
    role = models.ManyToManyField(Role, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    is_owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


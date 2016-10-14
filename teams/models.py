from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.timesince import timeuntil

from app.models import Organization

import datetime
import json


class Team(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    # Image upload is working for S3 bucket, but not for local environment (local development relies on connection to S3 at the moment)
    image = models.ImageField('img', upload_to='media/images/', default='img/dashboard_template_image.png')
    organization = models.ForeignKey(Organization, blank=True, null=True, default=None)

    @property
    def owners(self):
        return [member.user for member in self.member_set.filter(is_owner=True)]

    @property
    def members(self):
        return [member.user for member in self.member_set.all()]

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
            'description': self.description,
            'image': self.image.url,
            #TODO: add organization field
        }

    @property
    def jsoned(self):
        return json.dumps(self.to_dict())

    def save(self, *args, **kwargs):
        if not self.organization:
            # TODO: remove this block before going live
            raise AttributeError
        super(Team, self).save(*args, **kwargs)



class Role(models.Model):
    title = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    start_date = models.DateTimeField(default=None, blank=True, null=True)
    end_date = models.DateTimeField(default=None, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def to_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.strftime('%m-%d-%Y %H:%M'),
            'end_date': self.end_date.strftime('%m-%d-%Y %H:%M'),
            'duration': timeuntil(self.end_date, self.start_date),
            'start_date_str': self.start_date.strftime('%d %b').lstrip("0"),
        }

    @property
    def jsoned(self):
        return json.dumps(self.to_dict())


class Member(models.Model):
    role = models.ManyToManyField(Role, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    is_owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Invite(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='invites')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='inviteds')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    expired_at = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=20, default=None)
    read = models.BooleanField(default=False, blank=False, null=False)

    def to_dict(self):
        return {
            'id': self.pk,
            'status': self.status,
            'team': {
                'id': self.team.pk,
                'title': self.team.title
            },
            'inviter': {
                'id': self.inviter.pk,
                'name': self.inviter.profile.get_name()
            },
            'invitee': {
                'id': self.invitee.pk,
                'name': self.invitee.profile.get_name()
            }
        }


class JoinRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='team_join_requests')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    expired_at = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=20, default=None)
    read = models.BooleanField(default=False, blank=False, null=False)

    def to_dict(self):
        return {
            'id': self.pk,
            'status': self.status,
            'team': {
                'id': self.team.pk,
                'title': self.team.title
            },
            'requester': {
                'id': self.requester.pk,
                'name': self.requester.profile.get_name()
            }
        }
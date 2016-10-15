from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import get_thumbnail

import string, random


# Create your models here.
class Alert(models.Model):
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Lead(models.Model):
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class Organization(models.Model):
    name = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_by_user(user):
        return [membership.organization for membership in OrganizationMember.objects.filter(user=user)]

    @staticmethod
    def get_single_by_user(user):
        """
        This method will be useful only until the number organizations per users is limited to 1
        """
        organizations = Organization.get_by_user(user)
        if len(organizations) == 0:
            raise Organization.DoesNotExist
        return organizations[0]

    @property
    def members(self):
        return self.organizationmember_set.all()

    def __unicode__(self):
        return self.name


class OrganizationMember(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    is_owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class OrganizationInvitation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None, blank=True, null=True)
    email = models.EmailField(max_length=255, default='')
    token = models.CharField(max_length=64)
    expired = models.BooleanField(default=False)

    def __unicode__(self):
        return self.token

    def expire(self):
        self.expired = True
        self.save()

    def save(self, *args, **kwargs):
        try:
            _existing_invitation = OrganizationInvitation.objects.get(email=self.email)
            return None
        except self.DoesNotExist:
            pass
        # TODO: check if this token wasn't used before
        self.token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(64))
        super(OrganizationInvitation, self).save(*args, **kwargs)


class Token(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=64)
    type = models.CharField(max_length=16, default='password')
    expired = models.BooleanField(default=False)

    def __unicode__(self):
        return self.token

    def expire(self):
        self.expired = True
        self.save()

    def save(self, *args, **kwargs):
        # TODO: check if this token wasn't used before
        self.token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(64))
        super(Token, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    name = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    userpic = models.ImageField('img', upload_to='media/images/')
    bio = models.TextField(default='')

    def get_name(self):
        return self.name or self.user.email

    def get_location_string(self):
        return '%s%s%s' % (self.city, ', ' if self.city and self.country else '' , self.country)

    def to_dict(self):
        try:
            userpic_url = get_thumbnail(self.userpic, '300x300', crop='center', quality=99).url
        except AttributeError:
            userpic_url = 'http://placehold.it/300x300&text=Userpic'
        return {
            'id': self.user.pk,
            'name': self.get_name(),
            'location': self.get_location_string(),
            'userpic': userpic_url,
        }
    def get_teams_pks(self):
        return ','.join([str(team_membership.team.pk) for team_membership in self.user.member_set.all()])

    def get_userpic_url(self):
        if bool(self.userpic):
            return self.userpic.url
        else:
            return ''

from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Person(models.Model):
	profile=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	#ImageField depends on Pillow (pip install pillow)
	picture=models.ImageField(null=True, upload_to="media/profile_pics/%Y/%m/%d")
	fullname=models.CharField(max_length=100)
	bio=models.TextField()
	photo_url=models.CharField(max_length=800)

	def __str__(self):
		return self.fullname

class Membership(models.Model):
	organisation=models.CharField(max_length=100)
	organisation_url=models.CharField(max_length=100)
	bio=models.CharField(max_length=500)

	members=models.ManyToManyField(Person)

	def __str__(self):
		return self.organisation
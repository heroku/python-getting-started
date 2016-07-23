from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Person(models.Model):
	fullname=models.CharField(max_length=100)
	bio=models.CharField(max_length=1000)
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
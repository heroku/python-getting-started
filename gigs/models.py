from django.db import models
from django.contrib.auth.models import User
from people.models import Person
from datetime import datetime

# Create your models here.
class Gig(models.Model):
	title=models.CharField(max_length=55)
	description=models.TextField(null=True)
	owner=models.ForeignKey('auth.User', null=True)

	team=models.ManyToManyField(Person)

	start_date=models.DateTimeField(null=True)
	end_date=models.DateTimeField(null=True)

	created=models.DateTimeField(auto_now_add=True)
	modified=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	
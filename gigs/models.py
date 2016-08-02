from django.db import models
from django.contrib.auth.models import User
from people.models import Person
from datetime import datetime

# Create your models here.
class Gig(models.Model):
	title=models.CharField(max_length=55)
	description=models.TextField(null=True)
	admin=models.ManyToManyField('auth.User')

	team=models.ManyToManyField('auth.User', related_name='gig_team')

	start_date=models.DateTimeField(null=True)
	end_date=models.DateTimeField(null=True)

	created=models.DateTimeField(auto_now_add=True)
	modified=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title
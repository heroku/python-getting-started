from django.db import models
from django.contrib.auth.models import User
from people.models import Person
from datetime import datetime

# Create your models here.
class Gig(models.Model):
	title=models.CharField(max_length=55)
	description=models.TextField(null=True)

	start_date=models.DateTimeField(null=True)
	end_date=models.DateTimeField(null=True)

	created=models.DateTimeField(auto_now_add=True)
	modified=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class Role(models.Model):
	role=models.CharField(max_length=50)

	def __str__(self):
		return self.role

class Team(models.Model):
	person=models.ForeignKey(User, on_delete=models.CASCADE)
	gig=models.ForeignKey(Gig, on_delete=models.CASCADE)
	role=models.ForeignKey(Role, on_delete=models.CASCADE)

	def __str__(self):
		return "%s, of %s (%s)" % (self.person, self.gig, self.role)
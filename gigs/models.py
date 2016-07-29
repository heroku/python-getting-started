from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Gig(models.Model):
	title=models.CharField(max_length=55)
	description=models.TextField(null=True)
	owner=models.ForeignKey('auth.User', null=True)

	created=models.DateTimeField(auto_now_add=True)
	modified=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title
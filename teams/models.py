from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
	title=models.CharField(max_length=200)
	description=models.TextField(max_length=200)

	#Image upload has not been completed. Only very superficially tested between template and view. Does not utilise Django forms, either.
	image = models.ImageField('img', upload_to='media/images/', default='img/dashboard_template_image.png')

	owner=models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	def __str__(self):
		return self.title
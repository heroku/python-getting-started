from django.db import models

# Create your models here.
class Gig(models.Model):
	title=models.CharField(max_length=55)
	created=models.DateTimeField(auto_now_add=True)
	modified=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title
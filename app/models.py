from django.db import models


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

class Notification(models.Model):
	activity = models.CharField(max_length=100)
	activityId = models.IntegerField()
	expiredAt = models.DateTimeField(default=None, blank=True, null=True)
	read = models.BooleanField(default=False, blank=False, null=False)
from django.db import models
from django.contrib.auth.models import User
from people.models import Person
from datetime import datetime

# Create your models here.
class Message(models.Model):
	message=models.CharField(max_length=9999)
	date_sent=models.DateTimeField(auto_now_add=True)

	sent_from=models.ForeignKey(User, related_name='FromUser')
	sent_to=models.ForeignKey(User, related_name='ToUser')

	def __str__(self):
		return 'sent from: %s, to %s, on %s' % (self.sent_from, self.sent_to, self.date_sent)
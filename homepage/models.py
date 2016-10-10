from django.db import models


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Prospect(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

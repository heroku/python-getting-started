from django.contrib.gis.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class TestGeo(models.Model):
    geometry = models.GeometryField()
    point = models.PointField()
    mpoly = models.MultiPolygonField()

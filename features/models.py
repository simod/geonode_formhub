from django.db import models

from geonode.layers.models import Layer

class Feature(models.Model):

    lat = models.FloatField()
    lon = models.FloatField()

    layer = models.ForeignKey(Layer)

    image = models.ImageField(upload_to='features', blank=True, null=True)

    def __unicode__(self):
        return 'Feature'
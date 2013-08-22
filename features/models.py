from django.db import models

from geonode.layers.models import Layer

class Feature(models.Model):

    feature_id = models.IntegerField(primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()

    layer = models.ForeignKey(Layer)

    image = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return 'Feature'
import os
import httplib2

from django.db import models
from django.conf import settings

from geonode.layers.models import Layer

class Feature(models.Model):

    feature_id = models.IntegerField(primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()

    layer = models.ForeignKey(Layer)

    image = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return 'Feature of %s' % self.layer.typename

    def image_url(self):
        return "%s%s" % (settings.FORMHUB_MEDIA_URL, self.image)

    def small_image_url(self):
        h = httplib2.Http()
        image_name, ext = os.path.splitext(self.image)
        small_image_url =  "%s%s-small%s" % (settings.FORMHUB_MEDIA_URL, image_name, ext)
        resp, content = h.request(small_image_url, 'OPTIONS')
        if resp.status == 200:
            return small_image_url
        else:
            return self.image_url()
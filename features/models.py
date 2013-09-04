import os
import httplib2

from django.db import models
from django.conf import settings

from geonode.layers.models import Layer

from formhub.utils import datastore_connection

class Feature(models.Model):

    feature_id = models.IntegerField(primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()

    layer = models.ForeignKey(Layer)

    image = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return 'Feature of %s, %s' % (self.layer.typename, self.attribute())

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

    def attribute(self):
        connection = datastore_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM %s WHERE fid=%d' % (self.layer.name, self.feature_id))
        attributes = cursor.fetchall()
        cursor.close()
        connection.close()
        return ",".join(attributes[0][2:])
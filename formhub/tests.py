"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import json

from django.test import TestCase
from django.template.loader import render_to_string

from geonode.layers.models import Layer
from geonode.search.populate_search_test_data import create_models

from .views import compile_context, context_to_feature
from features.models import Feature

sample_context = json.loads('''{
    "hh_photo": "1377593318330.jpg", 
    "_id": 62, 
    "_attachments": [
        "user/attachments/1377593318330.jpg"
    ], 
    "name": "test", 
    "_submission_time": "2013-08-27T08:49:00", 
    "_uuid": "52d05214-3cb4-4c1f-b604-d3e4fcbb6a74", 
    "_bamboo_dataset_id": "", 
    "_deleted_at": null, 
    "_geolocation": ["45", "8"], 
    "hh_location": "45.810461095534265 8.6273552197963 160.79998779296875 25.0", 
    "_xform_id_string": "CA", 
    "_userform_id": "user_test", 
    "_status": "submitted_via_web", 
    "meta/instanceID": "uuid:52d05214-3cb4-4c1f-b604-d3e4fcbb6a74", 
    "formhub/uuid": "628d477db5a8407f8ea797d6b2982a0d"
}''')

class FormTests(TestCase):

    def setUp(self):
        create_models(type='layer')

    def test_get_valid_id(self):
        # TODO: this require postgis!
        pass

    def test_compile_context(self):
        # Test that upon a post submission the feature is inserted correctly

        context, image = compile_context(0,sample_context,[])

        self.assertEqual(context['lat'], '45')
        self.assertEqual(image, "user/attachments/1377593318330.jpg")
        template = render_to_string('formhub/transaction_insert.xml', context)
        self.assertTrue('<feature:CA' in template)

    def test_context_to_feature(self):

        layer = Layer.objects.get(name=sample_context['_xform_id_string'])
        context, image = compile_context(0,sample_context,[])
        feature = context_to_feature(layer, context, image)

        saved_feature = Feature.objects.get(feature_id=feature.pk)
        self.assertTrue(saved_feature.image, "user/attachments/1377593318330.jpg")
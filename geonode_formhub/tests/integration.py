import gisdata
import json

from django.conf import settings
from django.test import LiveServerTestCase as TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.management import call_command

from geonode.layers.utils import upload

from formhub.views import form_save

sample_context = '''{
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
    "_geolocation": "[45.810461095534265, 8.6273552197963]", 
    "hh_location": "45.810461095534265 8.6273552197963 160.79998779296875 25.0", 
    "_xform_id_string": "single_point", 
    "_userform_id": "user_test", 
    "_status": "submitted_via_web", 
    "meta/instanceID": "uuid:52d05214-3cb4-4c1f-b604-d3e4fcbb6a74", 
    "formhub/uuid": "628d477db5a8407f8ea797d6b2982a0d"
}'''

class FormhubFeatureTest(TestCase):
    """Tests geonode_formhub.formhub.form_save view
    """

    def setUp(self):
        call_command('loaddata', 'people_data', verbosity=0)
        upload(gisdata.VECTOR_DATA, console=None)

    def tearDown(self):
        pass

    def test_feature_post(self):
        c = Client()
        payload = json.loads(sample_context)
        url = reverse('fh-save')
        response = c.post(url, payload)
        self.assertEqual(response.status, 200)

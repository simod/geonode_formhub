"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.template.loader import render_to_string

test_context = {
    'fields': [
        {
        'name': u'name', 
        'value': u'Here'
        }
    ],
    'lat': u'45.81057869363576',
    'layer_name': u'fh_test',
    'lon': u'8.628644105046988'
}

class FormTests(TestCase):
    def test_transaction_template_rendering(self):
        """
        Tests that the transaction template is rendered properly
        """
        template = render_to_string('formhub/transaction_insert.xml', test_context)

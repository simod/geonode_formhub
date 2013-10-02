from django.conf.urls import include, patterns, url

urlpatterns = patterns(
    'geonode_formhub.features.views',
    url(r'^$', 'crowd_layers', name='crowd_layers'),
    url(r'^(?P<layername>[^/]*)/?$', 'crowd_layer_detail', name="crowd_layer_detail"),
)
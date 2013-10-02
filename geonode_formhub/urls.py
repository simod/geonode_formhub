from django.conf.urls import include, patterns
 
urlpatterns = patterns('',
    (r'^save/?$', include('geonode_formhub.formhub.urls')),
    (r'^crowd_layers/', include('geonode_formhub.features.urls')),
    )

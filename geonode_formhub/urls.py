from django.conf.urls import include, patterns
 
urlpatterns = patterns('',
    (r'^formhub/', include('formhub.urls')),
    (r'^crowd_layers/', include('features.urls')),
    )

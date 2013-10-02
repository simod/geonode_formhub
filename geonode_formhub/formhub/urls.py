from django.conf.urls import include, patterns, url

urlpatterns = patterns(
    'geonode_formhub.formhub.views',
    #url(r'^/?$', 'index', name='fh-index'),
    url(r'^/?$', 'form_save', name='fh-save'),
)
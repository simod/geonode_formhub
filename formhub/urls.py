from django.conf.urls import include, patterns, url

urlpatterns = patterns(
    'formhub.views',
    url(r'^/?$', 'index', name='fh-index'),
    url(r'^save/?$', 'form_save', name='fh-save'),
)
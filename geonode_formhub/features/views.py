from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

from geonode.layers.models import Layer
from geonode.layers.views import _resolve_layer, _PERMISSION_MSG_VIEW
from geonode.search.search import _filter_security

from .models import Feature

def crowd_layers(request, template='features/crowd_layers.html'):
    layers = Layer.objects.filter(pk__in=Feature.objects.distinct('layer').values('layer'))
    layers = _filter_security(layers, request.user, Layer, 'view_layer')
    return render_to_response(
        template,
        RequestContext(request, {
            "layers": layers,
            }
        )
    )

def crowd_layer_detail(request, layername, template='features/crowd_layer_detail.html'):
    layer = _resolve_layer(request, layername, 'layers.view_layer', _PERMISSION_MSG_VIEW)
    layer.json_url = layer.link_set.get(name='GeoJSON').url
    return render_to_response(template, RequestContext(request, {
        "layer": layer,
        "features": layer.feature_set.all(),  
    }))
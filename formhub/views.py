import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.http import require_POST

from geonode.utils import check_geonode_is_up
from geonode.layers.models import Layer

from .utils import Gs_client
from features.models import Feature

wfs_url = settings.GEOSERVER_BASE_URL + "wfs/WfsDispatcher?"

def index(req):
    pass

def compile_context(req_body, attributes):
    context = {
            'fields': []
        }
    for a in attributes:
        # For each attribute in the layer look for the correspondent in the form
        # TODO: do it safely
        if a.attribute != 'the_geom' and a.attribute != 'id':
            context['fields'].append(
                {
                'name': a.attribute,
                'value': req_body[a.attribute]
                }
            )
    lat = req_body['_geolocation'][0] if req_body['_geolocation'][0] is not None else 0
    lon = req_body['_geolocation'][1] if req_body['_geolocation'][1] is not None else 0
    context['lat'] = lat
    context['lon'] = lon
    context['layername'] = req_body['_xform_id_string']
    context['id'] = req_body['_id']
    return context

@csrf_exempt
@require_POST
def form_save(req):
    
    check_geonode_is_up()

    body = json.loads(req.body)
    
    geoserver = Gs_client(wfs_url)

    layername = body['_xform_id_string']
    try:
        layer = Layer.objects.get(title=layername)
    except Layer.DoesNotExist:
        raise Layer.DoesNotExist

    attributes = layer.attribute_set.all()
    
    context = compile_context(body, attributes)
    
    template = render_to_string('formhub/transaction_insert.xml',context)
    try:
        response = geoserver.client.request(wfs_url, method='POST', body=template)
        geoserver.updatebounds(layername)
        layer.update_thumbnail()
        return HttpResponse('Inserted')
    except:
        raise 
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from geonode.utils import check_geonode_is_up
from geonode.layers.models import Layer

from .utils import Gs_client, get_valid_id, check_feature_store, check_user
from geonode_formhub.features.models import Feature

def index(req):
    pass

def compile_context(valid_id, req_body, attributes):
    context = {
            'fields': []
        }
    image = None
    for a in attributes:
        # For each attribute in the layer look for the correspondent in the form
        # TODO: do it safely
        if a.attribute != 'the_geom' and a.attribute != 'id' and a.attribute != 'image':
            context['fields'].append(
                {
                'name': a.attribute,
                'value': req_body[a.attribute]
                }
            )
    if len(req_body['_attachments']) > 0:
        image = req_body['_attachments'][0]

    lat = req_body['_geolocation'][0] if req_body['_geolocation'][0] is not None else 0
    lon = req_body['_geolocation'][1] if req_body['_geolocation'][1] is not None else 0
    context['lat'] = lat
    context['lon'] = lon
    context['layername'] = req_body['_xform_id_string']
    context['id'] = valid_id

    return context, image

@csrf_exempt
@require_POST
def form_save(req):
    check_geonode_is_up()

    if not check_feature_store():
        raise ValueError('No postgis database found.')
    
    layername = req.POST.get('_xform_id_string', None)
    if not layername: 
        # Normal post from odk
        body = json.loads(req.body)
        layername = body['_xform_id_string']
    else:
        # Test environment
        body = req.POST.dict()
        body['_geolocation'] = json.loads(body['_geolocation'])

    try:
        layer = Layer.objects.get(name=layername)
    except Layer.DoesNotExist:
        raise Layer.DoesNotExist

    if not check_user(body['_userform_id'].split('_')[0],  layer):
        raise ValueError('User not found in the database')

    # Don't trust the id from ODK, look into the db sequence to get the right one
    valid_id = get_valid_id(layername)
    # Guess the list of fields from the layer's attributes
    attributes = layer.attribute_set.all()
    # Compile the context
    context, image = compile_context(valid_id, body, attributes)
    template = render_to_string('formhub/transaction_insert.xml',context)

    # Instanciate the client and post the insert request
    geoserver = Gs_client()
    try:
        response = geoserver.client.request(geoserver.wfs_url, method='POST', body=template)

        #Update the layer bounds and the thumbnail
        geoserver.updatebounds(layername)
        layer.update_thumbnail()
        context_to_feature(layer, context, image)
        return HttpResponse('Inserted')
    except:
        raise 

def context_to_feature(layer, context, image):
    """ Write the feature with the image to the database
    """
    try:
        f = Feature.objects.create(
            feature_id = context['id'],
            lat = context['lat'],
            lon = context['lon'],
            layer = layer,
            image = image
            )
        return f
    except:
        raise

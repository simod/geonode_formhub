import json
import psycopg2

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.http import require_POST

from geonode.utils import check_geonode_is_up
from geonode.layers.models import Layer

from .utils import Gs_client
from features.models import Feature

wfs_url = settings.OGC_SERVER['default']['LOCATION'] + "wfs/WfsDispatcher?"

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
    # Don't trust the id from ODK, look into the db sequence to get the right one
    valid_id = get_valid_id(layername)
    attributes = layer.attribute_set.all()
    context, image = compile_context(valid_id, body, attributes)
    template = render_to_string('formhub/transaction_insert.xml',context)

    # Instanciate the client and post the insert request
    geoserver = Gs_client(wfs_url)
    try:
        response = geoserver.client.request(wfs_url, method='POST', body=template)

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
        Feature.objects.create(
            feature_id = context['id'],
            lat = context['lat'],
            lon = context['lon'],
            layer = layer,
            image = image
            )
        return True
    except:
        raise

def get_valid_id(layername):
    """ Get a valid id from the layer sequence from the database
    """
    connection = psycopg2.connect(
        host=settings.DATABASES['datastore']['HOST'],
        database=settings.DATABASES['datastore']['NAME'],
        user=settings.DATABASES['datastore']['USER'],
        password=settings.DATABASES['datastore']['PASSWORD'],
        port=settings.DATABASES['datastore']['PORT']
    )
    cursor=connection.cursor()
    cursor.execute('SELECT last_value FROM %s_fid_seq;' % layername)
    valid_id = cursor.fetchone()[0] + 1
    cursor.close()
    connection.close()
    return valid_id

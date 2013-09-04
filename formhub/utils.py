import httplib2
import psycopg2

from urlparse import urlparse

from django.conf import settings
from django.contrib.auth.models import User


class Gs_client(object):

    def __init__(self, url):
        self._user = settings.OGC_SERVER['default']['USER']
        self._password = settings.OGC_SERVER['default']['PASSWORD']
        self.gs_url = settings.OGC_SERVER['default']['LOCATION']
        self.client = self.get_client(url)

    def get_client(self, url):
        
        http_client = httplib2.Http()
        http_client.add_credentials(self._user, self._password)
        _netloc = urlparse(url).netloc
        http_client.authorizations.append(
            httplib2.BasicAuthentication(
                (self._user, self._password),
                _netloc,
                self.gs_url,
                {},
                None,
                None,
                http_client
            )
        )

        return http_client

    def updatebounds(self, layername):
        
        url = "%srest/workspaces/geonode/datastores/%s/featuretypes/%s.xml?recalculate=nativebbox,latlonbbox" \
                % (self.gs_url, settings.DATABASES['datastore']['NAME'], layername)

        data = '''<featureType>
                    <name>%s</name>
                    <enabled>true</enabled>
                </featureType>''' % layername
        
        headers = {'Content-type': 'text/xml'}
        
        try:
            self.client.request(url, method='PUT', body=data, headers=headers)
        except:
            raise Exception("Geoserver error when updating bounds")

def datastore_connection():
    datastore = settings.OGC_SERVER['default']['OPTIONS']['DATASTORE']
    db = settings.DATABASES[datastore]
    connection = psycopg2.connect(
        host=db['HOST'],
        database=db['NAME'],
        user=db['USER'],
        password=db['PASSWORD'],
        port=db['PORT']
    )
    return connection

def get_valid_id(layername):
    """ Get a valid id from the layer sequence from the database
    """
    connection = datastore_connection()
    cursor=connection.cursor()
    cursor.execute('SELECT last_value FROM %s_fid_seq;' % layername)
    valid_id = cursor.fetchone()[0] + 1
    cursor.close()
    connection.close()
    return valid_id

def check_feature_store():
    datastore = settings.OGC_SERVER['default']['OPTIONS']['DATASTORE']
    if not 'postgis' in settings.DATABASES[datastore]['ENGINE']:
        return False
    else:
        return True

def check_user(username, layer):

    user = User.objects.get(username=username)
    return user.has_perm('layers.change_layer', obj=layer)





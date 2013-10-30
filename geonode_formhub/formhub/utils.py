import httplib2
import psycopg2

from urlparse import urlparse

from django.conf import settings
from django.contrib.auth.models import User

from geonode.utils import ogc_server_settings


class Gs_client(object):

    def __init__(self):
        self._user, self._password = ogc_server_settings.credentials
        self.gs_url = ogc_server_settings.public_url
        self.wfs_url = ogc_server_settings.public_url + "wfs/WfsDispatcher?"
        self.client = self.get_client()

    def get_client(self):
        
        http_client = httplib2.Http()
        http_client.add_credentials(self._user, self._password)
        _netloc = urlparse(self.wfs_url).netloc
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
        """ 
        Updates the bounds of the layer in geoserver.
        """
        url = "%srest/workspaces/geonode/datastores/%s/featuretypes/%s.xml?recalculate=nativebbox,latlonbbox" \
                % (self.gs_url, ogc_server_settings.datastore_db['NAME'], layername)

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
    """
    Creates a connection to the db datastore.
    """
    datastore = ogc_server_settings.datastore_db
    connection = psycopg2.connect(
        host=datastore['HOST'],
        database=datastore['NAME'],
        user=datastore['USER'],
        password=datastore['PASSWORD'],
        port=datastore['PORT']
    )
    return connection

def get_valid_id(layername):
    """ 
    Get a valid id from the layer sequence from the database
    """
    connection = datastore_connection()
    cursor=connection.cursor()
    cursor.execute('SELECT last_value FROM %s_fid_seq;' % layername)
    valid_id = cursor.fetchone()[0] + 1
    cursor.close()
    connection.close()
    return valid_id

def check_feature_store():
    """
    Check that the postgis datastore is configured correctly
    """
    datastore = ogc_server_settings.datastore_db
    if not ogc_server_settings.datastore_db.get('ENGINE') \
        or not 'postgis' in datastore['ENGINE']:
        return False
    else:
        return True

def check_user(username, layer):

    user = User.objects.get(username=username)
    return user.has_perm('layers.change_layer', obj=layer)

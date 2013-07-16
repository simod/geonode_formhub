import httplib2

from urlparse import urlparse

from django.conf import settings

def get_client(url):
    
    _user, _password = settings.GEOSERVER_CREDENTIALS

    http_client = httplib2.Http()
    http_client.add_credentials(_user, _password)
    http_client.add_credentials(_user, _password)
    _netloc = urlparse(url).netloc
    http_client.authorizations.append(
        httplib2.BasicAuthentication(
            (_user, _password),
            _netloc,
            settings.GEOSERVER_BASE_URL,
            {},
            None,
            None,
            http_client
        )
    )

    return http_client

def updatebounds(layername):
    
    url = "%srest/workspaces/geonode/datastores/%s/featuretypes/%s.xml?recalculate=nativebbox,latlonbbox" \
            % (settings.GEOSERVER_BASE_URL, settings.DB_DATASTORE_NAME, layername)

    data = '''<featureType>
                <name>%s</name>
                <enabled>true</enabled>
                </featureType>''' % layername
    
    headers = {'Content-type': 'text/xml'}
    
    http_client= get_client(url)

    try:
        r = http_client.request(url, method='PUT',body=data, headers=headers))
    except:
        raise Exception("Geoserver error when updating bounds")
import httplib2

from urlparse import urlparse

from django.conf import settings


class Gs_client(object):

    def __init__(self, url):
        self._user, self._password = settings.GEOSERVER_CREDENTIALS
        self.gs_url = settings.GEOSERVER_BASE_URL
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
                % (self.gs_url, settings.DB_DATASTORE_NAME, layername)

        data = '''<featureType>
                    <name>%s</name>
                    <enabled>true</enabled>
                </featureType>''' % layername
        
        headers = {'Content-type': 'text/xml'}
        
        try:
            self.client.request(url, method='PUT', body=data, headers=headers)
        except:
            raise Exception("Geoserver error when updating bounds")
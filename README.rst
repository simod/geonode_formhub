Geonode Formhub
========================

GeoNode extension to integrate data coming from ODK/Formhub.

Installation of the extension development mode
----------------------------------------------

    $ git clone https://github.com/simod/geonode_formhub.git@no-project

Activate the geonode virtualenv

    $ pip install -e geonode_formhub

Add the following apps to your installed apps: 

    'geonode_formhub.features',

    'geonode_formhub.formhub',

Syncd the database
    
    $ python manage.py syncdb

Add the following in the urls.py file:

    (r'^formhub/', include('geonode_formhub.urls')),

Add the content of the geonode_formhub/local_setting.sample to your local settings.

Add the content of geonode_formhub/templates/base.html to the geonode/tempaltes/base.html template.

Setup formhub
-------------

Install Formhub following https://github.com/modilabs/formhub.

Create a proxy in apache::

    ProxyPass / http://192.168.2.1:8000/
    ProxyPassReverse / http://192.168.2.1:8000/

Start apache and open a network share through the wi-fi device.

Modify the file my_geonode/geoserver/data/security/auth/geonodeAuthProvider/config.xml and set the port to 8001

Start Formhub::

    $ python manage.py runserver 192.168.2.1:8000

Start GeoNode::
    
    $ paver start_geoserver 
    $ python manage.py runserver 8001

Install ODK on your android mobile and connect it to the shared network.

Usage
---------

In order to be Formhub compliant the layer must be on postgis (GeoNode's DB_DATASTORE=True) and must be a POINT layer.

Create and upload a form that match the layer name in GeoNode with the same fields plus a coordinate field and an image field (refer to the Formhub guide for this https://formhub.org/syntax/).

In the Form page set a rest service as JSON post to http://localhost:8001/formhub/save

On your mobile, in ODK set the address to http://192.168.2.1/youruser

Start submitting.

The submissions will appear in the Crowd Layers tab of GeoNode.


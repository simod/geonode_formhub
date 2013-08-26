Geonode_Formhub
========================

GeoNode extension to integrate data coming from ODK/Formhub.

Installation in development/testing mode
------------

Create a new virtualenv for geonode_formhub, install GeoNode and setup your project::

    $ mkvirtualenv my_geonode
    $ pip install Django
    $ django-admin.py startproject my_geonode --template=https://github.com/simod/geonode_formhub/archive/master.zip -epy,rst 
    $ pip install -e my_geonode

To install the latest from GeoNode's master branch use the following command::

    $ pip install -e git+https://github.com/GeoNode/geonode.git#egg=geonode --upgrade

Install Formhub following https://github.com/modilabs/formhub.

Create a proxy in apache:

    ProxyPass / http://192.168.2.1:8000/
    ProxyPassReverse / http://192.168.2.1:8000/

Start apache and open a network share through the wi fi device.

Modify the file my_geonode/geoserver/data/security/auth/geonodeAuthProvider/config.xml and set the port to 8001

Start Formhub: 

    $ python manage.py runserver 192.168.2.1:8000

Start GeoNode:
    
    $ paver start_geoserver 
    $ python manage.py runserver 8001

Install ODK on your android mobile and connect it to the shared network.

Usage
---------

In order to be Formhub compliant the layer must be on postgis (GeoNode's DB_DATASTORE=True) and must be a POINT layer.

Create and upload a form that match the layer in GeoNode with the same fields plus if a coordinate field and an image field (refer to the Formhub guide for this https://formhub.org/syntax/).

In the Form page set a rest service to http://localhost:8001/formhub/save

In ODK set the address to http://192.168.2.1/youruser

Start submitting.

The submissions will appear in the Crowd Forms tab of GeoNode.


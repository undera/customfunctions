Additional functions for graphite-web
===============

To install it:
    sudo git clone https://github.com/undera/customfunctions.git /usr/lib/python2.7/customfunctions
    echo "from graphite.app_settings import *" | sudo tee -a /opt/graphite/webapp/graphite/local_settings.py
    echo "INSTALLED_APPS+=('customfunctions',)" | sudo tee -a /opt/graphite/webapp/graphite/local_settings.py
    sudo service apache2 restart



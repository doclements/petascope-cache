from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from petascope_cache import settings
from petascope_cache.core import setup_routing

# setup application
app = Flask('petascope_cache')
app.config.from_object(settings)

import logging
from logging.handlers import RotatingFileHandler
f_handler = RotatingFileHandler('/local1/data/backup/rsgadmin/earthserver.pml.ac.uk/cache_app/test.log')
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(filename)s:%(lineno)d]'
))
app.logger.addHandler(f_handler)


# setup database
db = SQLAlchemy(app)

#dict of mime-types. key = representation used in wcps, 
#value = tuple(internet standard mime-type, file suffix)
mime_types = {'png' : ('image/png', 'png'),
              'jpg' : ('image/jpeg','jpeg'),
              'jpeg' : ('image/jpeg','jpeg'),
              'csv' : ('text/csv', 'csv'),
              'netcdf' : ('x-netcdf', 'nc'),
              'tiff' : ('image/tiff', 'tif')}


# register application views and blueprints
from petascope_cache.urls import routes
setup_routing(app, routes)

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

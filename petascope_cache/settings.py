#change me to False before using in production
DEBUG = True
SECRET_KEY = 'CHANGE ME TO SOMETHING SECRET!!!!!'

#path to sqlite database
SQLALCHEMY_DATABASE_URI = 'sqlite://///path/to/cached/images/database/peta_cache.db'
#URL for your petascope instance
PETASCOPE_BASE = 'http://earthserver.pml.ac.uk/petascope'
#location for storing the database and cached images
IMAGE_CACHE = '/path/to/cached/images/directory/'

import logging
#change to ERROR when deployed in production
LOGGING_LEVEL = logging.DEBUG
#cache time to keep in days
CACHE_TIME_TO_KEEP = 86400

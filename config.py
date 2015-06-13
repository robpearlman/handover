#config.py 

import os

#get where folder sits

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'handover.db'
CSRF_ENABLED = True
SECRET_KEY = '9bc4e9c5c22c2e1fb2be2a218f434a37'

#get full path for db

DATABASE_PATH = os.path.join(basedir, DATABASE)

#SQLAlchemy uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

DEBUG  = True
#DEBUG  = False
#!flask/bin/python
'Script to create the database'

from migrate.versioning import api
from config import config
from app import db, create_app
import os.path

SQLALCHEMY_DATABASE_URI = config['default'].SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config['default'].SQLALCHEMY_MIGRATE_REPO

create_app('default')
db.create_all(app=create_app('default'))
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
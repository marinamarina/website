#!flask/bin/python
'Script to migrations the database'

import imp
from migrate.versioning import api
from config import config
from app import db, create_app
import os.path

SQLALCHEMY_DATABASE_URI = config['default'].SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config['default'].SQLALCHEMY_MIGRATE_REPO

create_app('default')
db.create_all(app=create_app('default'))

migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'New migration saved as ' + migration
print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))
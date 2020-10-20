import logging

#import connexion
from flask_testing import TestCase
from flask import g
from flask_sqlalchemy import SQLAlchemy

from imprcm_uuid_server import db, startup
#from flask_sqlalchemy import SQLAlchemy


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        self.test_app = startup.create_cnxn_app(spec_dir='./swagger', db_url='sqlite://')
        return self.test_app.app


    def setUp(self):
        db.the_db.create_all(app=self.test_app.app)

        # put in some basic reference data to be used by tests
        with self.test_app.app.app_context():
            scheme = db.Scheme(scheme_url='evn', scheme_name='European Vehicle Number')
            db.the_db.session.add(scheme)
            db.the_db.session.commit()
            #print(db.the_db.session.query(db.Scheme).all())

    
    def tearDown(self):
        with self.test_app.app.app_context():
            db.the_db.session.remove()
            db.the_db.drop_all()

#	homebrew assertion
	#def assertKeyMissingOrSame(:


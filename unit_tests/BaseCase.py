
import unittest

from app import app, db
from models import User, Bookmark

class BaseCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # db.init_app(app)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

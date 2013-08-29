import unittest
from datetime import date, datetime, timedelta
import transaction

from .models import Notification
from . import api

from .config import config

"""
I've got a class defined in test_f which does the following.

class DBTestClass(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = routes(testing.setUp())
    
    def tearDown(self):
        DBSession.execute("ROLLBACK")
        self.session.remove()
    
    def get_app(self, auth):
        # Auth is a username of the user you're authing as
        # Code that returns a testapp and cookie data
    
    def make_request(self, app, path, data, msg="", expect_forward=False):
        # Makes a request and checks for errors
        # Provides a custome message on failure
        # Allows expected fowards

Sadly I couldn't work out how to detatch this part from my
main framework. The key part is it'll allow us to use the db connection.
"""

try:
    from ..core.lib.test_f import DBTestClass
except Exception:
    class DBTestClass(object):
        pass

# We assume this is the user your system will grab for us
user_id = 1

class NotificationTester(DBTestClass):
    def test_lifecycle(self):
        r_true = lambda r, x: True
        r_false = lambda r, x: False
        r_id = lambda r, x: x
        
        # Reset handlers, just to be sure
        config['handlers'] = {}
        
        # We'll need these later
        app, cookies = self.get_app()
        
        # Register them, the test_register function below tests the accuracy of this
        api.register('test_true', 'Title', 'image', r_true)
        api.register('test_false', 'Title', 'image', r_false)
        api.register('test_id', 'Title', 'image', r_id)
        
        now = datetime.today() + timedelta(hours=36)
        
        # Clear all existing notifications
        config['DBSession'].execute('DELETE FROM notifications')
        
        # Make sure that worked
        notification_list = list(config['DBSession'].query(Notification))
        self.assertEqual(len(notification_list), 0)
        
        # Insert
        api.send(user=user_id, category="test_true", message="Test message", data="Data", expires=timedelta(hours=4))
        api.send(user=user_id, category="test_false", message="Test message", data="Data", expires=date(year=now.year, month=now.month, day=now.day))
        api.send(user=user_id, category="test_id", message="Test message", data="Data", expires=now)
        api.send(user=user_id, category="test_id", message="Test message", data="Data 2", expires=now, avoid_duplicates=True)
        
        # Check all of them got added
        notification_list = list(config['DBSession'].query(Notification).order_by(Notification.id.asc()))
        self.assertEqual(len(notification_list), 3)
        
        n1, n2, n3 = notification_list
        
        config['DBSession'].execute("COMMIT")
        
        # Test viewing process
        page_result = self.make_request(
            app,
            "/communique/view/{}".format(n1.id),
            cookies,
            "There was an error viewing the first notification"
        )
        self.assertEqual(str(page_result), "Response: 200 OK\nContent-Type: text/plain; charset=UTF-8\nTrue")
        
        # Test mini home
        page_result = self.make_request(
            app,
            "/communique/mini_home",
            cookies,
            "There was an error viewing the mini home"
        )
        
        page_result = self.make_request(
            app,
            "/communique/home_count/{}".format(user_id),
            cookies,
            "There was an error viewing the home count"
        )
        self.assertEqual(str(page_result), "Response: 200 OK\nContent-Type: text/plain; charset=UTF-8\n2")
        
        # Test remaining views
        page_result = self.make_request(
            app,
            "/communique/view/{}".format(n2.id),
            cookies,
            "There was an error viewing the first notification"
        )
        self.assertEqual(str(page_result), "Response: 200 OK\nContent-Type: text/plain; charset=UTF-8\nFalse")
        
        page_result = self.make_request(
            app,
            "/communique/view/{}".format(n3.id),
            cookies,
            "There was an error viewing the first notification"
        )
        self.assertEqual(str(page_result), "Response: 200 OK\nContent-Type: text/plain; charset=UTF-8\nData")

class FunctionTester(unittest.TestCase):
    def test_register(self):
        r_true = lambda r, x: True
        r_false = lambda r, x: False
        r_id = lambda r, x: x
        
        # Reset handlers, just to be sure
        config['handlers'] = {}
        
        api.register('test_true', 'Title', 'image', r_true)
        api.register('test_false', 'Title', 'image', r_false)
        api.register('test_id', 'Title', 'image', r_id)
        
        # Check it won't let us overwrite an existing registrant
        self.assertRaises(KeyError, api.register, 'test_true', 'Title', 'image', r_true, raise_on_dupe=True)
        
        self.assertEqual(len(config['handlers']), 3)
        self.assertIn('test_false', config['handlers'])
        self.assertNotIn('test_not_in', config['handlers'])

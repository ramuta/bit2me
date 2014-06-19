from auth import generate_token, validate_token
import unittest
from google.appengine.ext import testbed
from secrets import secret_string


# write your tests here
# run tests with: python tests.py
class TestHandlers(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    '''
    def test_main_handler(self):
        request = webapp2.Request.blank('/')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, 'Hello, world!')
    '''

    def test_token(self):
        token = generate_token(userid='12345', secret=secret_string)
        self.assertTrue(validate_token(token=token, secret=secret_string))


# key part - don't delete
def main():
    unittest.main()

if __name__ == '__main__':
    main()
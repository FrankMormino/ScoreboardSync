# In your test_auth.py file:
import unittest
from app.auth import app
from flask import url_for

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_google_login(self):
        response = self.app.get(url_for('login_google'))
        mock_google.authorize.return_value = 'Mock Google Authorization'
        response = self.app.get(url_for('login_google'))
        self.assertEqual(response.data.decode(), 'Mock Google Authorization')

    def test_outlook_login(self):
        response = self.app.get(url_for('login_outlook'))
        mock_outlook.authorize.return_value = 'Mock Outlook Authorization'
        response = self.app.get(url_for('login_outlook'))
        self.assertEqual(response.data.decode(), 'Mock Outlook Authorization')

if __name__ == '__main__':
    unittest.main()

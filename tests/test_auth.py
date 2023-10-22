import unittest
from unittest.mock import patch
from flask import url_for
from app.auth import app

class TestAuth(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('app.auth.google')
    def test_google_login(self, mock_google):
        mock_google.authorize.return_value = 'Mock Google Authorization'
        response = self.app.get(url_for('login_google'))
        self.assertEqual(response.data.decode(), 'Mock Google Authorization')

    @patch('app.auth.outlook')
    def test_outlook_login(self, mock_outlook):
        mock_outlook.authorize.return_value = 'Mock Outlook Authorization'
        response = self.app.get(url_for('login_outlook'))
        self.assertEqual(response.data.decode(), 'Mock Outlook Authorization')

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
from flask import url_for, session
from app.calendar_integration import app

class TestCalendarIntegration(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.calendar_integration.google')
    def test_fetch_google_events(self, mock_google):
        with self.app.session_transaction() as sess:
            sess['google_token'] = ('mock_token', '')
        mock_google.get.return_value = 'Mock Google Events'
        response = self.app.get(url_for('fetch_google_events'))
        self.assertEqual(response.data.decode(), 'Mock Google Events')

    @patch('app.calendar_integration.requests.get')
    def test_fetch_outlook_events(self, mock_get):
        with self.app.session_transaction() as sess:
            sess['outlook_token'] = ('mock_token', '')
        mock_get.return_value.json.return_value = 'Mock Outlook Events'
        response = self.app.get(url_for('fetch_outlook_events'))
        self.assertEqual(response.data.decode(), 'Mock Outlook Events')

if __name__ == '__main__':
    unittest.main()

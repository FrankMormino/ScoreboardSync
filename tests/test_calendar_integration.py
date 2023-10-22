import unittest
from app.calendar_integration import fetch_google_events  # assuming fetch_google_events is a function in your module

class TestCalendarIntegration(unittest.TestCase):

    def test_fetch_google_events(self):
        events = fetch_google_events()
        # assuming events is a list of event dictionaries
        self.assertIsInstance(events, list)
        if events:  # check the structure of an event if there are any events
            self.assertIn('summary', events[0])

if __name__ == '__main__':
    unittest.main()

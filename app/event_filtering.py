from app.calendar_integration import fetch_google_events, fetch_outlook_events
import re


def filter_events(events):
    filtered_events = []
    for event in events:
        title = event.get('summary', '').lower()
        # Assuming sports events have a common keyword like "game" or "match" in the title
        if re.search(r'\b(game|match)\b', title):
            filtered_events.append(event)
    return filtered_events


def fetch_and_filter_events():
    # Assume google_events and outlook_events are the lists of events retrieved from Google and Outlook
    google_events = fetch_google_events()
    outlook_events = fetch_outlook_events()

    # Filter the events
    filtered_google_events = filter_events(google_events)
    filtered_outlook_events = filter_events(outlook_events)

    return filtered_google_events, filtered_outlook_events

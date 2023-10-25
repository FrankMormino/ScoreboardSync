import json

from app.calendar_integration import fetch_google_events, fetch_outlook_events
import re


def filter_events(events):
    filtered_events = []
    for event in events:
        title = event.get('summary', '').lower()
        # Assuming sports events have a common keyword like "game" or "match" or "practice" in the title, and we want
        # it to be case-insensitive
        if re.search(r'\b(game|match|practice)\b', title, re.IGNORECASE):
            filtered_events.append(event)
    return filtered_events


def fetch_and_filter_events():
    # Assume google_events and outlook_events are the lists of events retrieved from Google and Outlook
    try:
        google_events = json.loads(fetch_google_events())  # json.loads() converts a JSON string to a Python object
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Google: {e}")  # Log the error for debugging
        google_events = []  # Return an empty list if there's an error

    try:
        outlook_events = json.loads(fetch_outlook_events())
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Outlook: {e}")
        outlook_events = []

    # Filter the events
    filtered_google_events = filter_events(google_events)
    filtered_outlook_events = filter_events(outlook_events)

    return filtered_google_events, filtered_outlook_events

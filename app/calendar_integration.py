# Description: This file contains the routes for the calendar integration
# File name: calendar_integration.py


from flask import Blueprint, session, redirect, url_for
from app.auth import google  # Import the OAuth setups from auth.py
from google.oauth2 import credentials
from googleapiclient.discovery import build
import datetime
import os  # Import the os module
from app.auth import google, get_google_oauth_token  # Import the OAuth setups and token getter from auth.py
from flask import Blueprint, session, redirect, url_for
import requests
from google.auth.transport.requests import Request  # Import the Request class
from google.oauth2.credentials import Credentials  # Import the Credentials class
from googleapiclient.errors import HttpError  # Import the HttpError class

calendar_integration = Blueprint('calendar_integration', __name__)


@calendar_integration.route('/fetch_google_events')
def fetch_google_events():
    # Check if the token file exists and load the credentials from it
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar.readonly'])
        # If there are no (valid) credentials available, redirect to login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Save the refreshed credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            else:
                return redirect(url_for('auth.login_google'))

        try:
            # Build the Google Calendar API client
            service = build('calendar', 'v3', credentials=creds)
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = service.events().list(
                calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            return str(events)  # Convert to string for simple display

        except HttpError as error:
            print(f'An error occurred: {error}')  # Log the error for debugging
            return f'Error: {error}', 500  # Return a 500 Internal Server Error response

    return redirect(url_for('auth.login_google'))  # Redirect to the login page if necessary



@calendar_integration.route('/fetch_outlook_events')
def fetch_outlook_events():
    if 'outlook_token' in session:
        token = session['outlook_token'][0]  # Assume token is stored as a tuple
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
            'Prefer': 'outlook.body-content-type="text"',
        }
        outlook_api_endpoint = 'https://graph.microsoft.com/v1.0/me/events'
        response = requests.get(outlook_api_endpoint, headers=headers)  # Use requests to make the API call
        if response.status_code == 200:
            events = response.json()
            return str(events)  # Convert to string for simple display
        else:
            return f'Error: {response.status_code}', response.status_code  # Handle error responses
    return redirect(url_for('auth.login_outlook'))  # in fetch_outlook_events

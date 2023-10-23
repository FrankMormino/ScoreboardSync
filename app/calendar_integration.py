from flask import Blueprint, session, redirect, url_for
from app.auth import google  # Import the OAuth setups from auth.py
from google.oauth2 import credentials
from googleapiclient.discovery import build
import datetime
import os  # Import the os module
from app.auth import google, get_google_oauth_token  # Import the OAuth setups and token getter from auth.py
from flask import Blueprint, session, redirect, url_for
import requests

calendar_integration = Blueprint('calendar_integration', __name__)


@calendar_integration.route('/fetch_google_events')
def fetch_google_events():
    if 'google_token' in session:
        token_tuple = get_google_oauth_token()
        if not token_tuple:
            return redirect(url_for('auth.login_google'))  # Redirect to the login page if necessary

        access_token, refresh_token = token_tuple  # Unpack the token tuple

        # Construct the token_info dictionary
        token_info = {
            'token': access_token,
            'refresh_token': refresh_token,  # Use the refresh token from the session
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
            'scopes': 'https://www.googleapis.com/auth/calendar.readonly'
        }


        # Create a Credentials object
        creds = credentials.Credentials.from_authorized_user_info(token_info)

        # Build the Google Calendar API client
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return str(events)  # Convert to string for simple display
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

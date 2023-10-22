from flask import Flask, request, session, redirect, url_for
from auth import google, outlook  # Import the OAuth setups from auth.py
import datetime
from googleapiclient.discovery import build
import requests  # Import the requests library
import os

app = Flask(__name__)

# Make sure to have secret key for session management
app.secret_key = os.environ.get('FLASK_SECRET_KEY')  # Use the environment variable for your secret key

@app.route('/fetch_google_events')
def fetch_google_events():
    if 'google_token' in session:
        credentials = google.get('credentials')  # Obtain credentials from the OAuth object
        if credentials:
            service = build('calendar', 'v3', credentials=credentials)
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = service.events().list(
                calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            return str(events)  # Convert to string for simple display
    return redirect(url_for('login_google'))

@app.route('/fetch_outlook_events')
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
    return redirect(url_for('login_outlook'))

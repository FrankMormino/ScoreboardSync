from flask import Flask, request, session, redirect, url_for
from auth import google, outlook  # Import the OAuth setups from auth.py
import datetime
from googleapiclient.discovery import build
import msal

app = Flask(__name__)

# Make sure to have secret key for session management
app.secret_key = 'your_secret_key_here'
@app.route('/fetch_google_events')
def fetch_google_events():
    if 'google_token' in session:
        credentials = google.tokengetter_func(token=session.get('google_token'))
        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return str(events)  # Convert to string for simple display
    return redirect(url_for('login_google'))

@app.route('/fetch_outlook_events')
def fetch_outlook_events():
    if 'outlook_token' in session:
        token = session['outlook_token']['access_token']
        client = msal.ConfidentialClientApplication(
            'YOUR_OUTLOOK_CLIENT_ID',
            client_credential='YOUR_OUTLOOK_CLIENT_SECRET',
            authority='https://login.microsoftonline.com/common'
        )
        outlook_api_endpoint = 'https://graph.microsoft.com/v1.0/me/events'
        response = client.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"],)
        events = response.json()
        return str(events)  # Convert to string for simple display
    return redirect(url_for('login_outlook'))

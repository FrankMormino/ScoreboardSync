from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
import os

# Initialize Flask app and OAuth
app = Flask(__name__)
oauth = OAuth(app)

# Set up Google OAuth
google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/calendar.readonly',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Set up Outlook OAuth
outlook = oauth.remote_app(
    'outlook',
    consumer_key=os.environ.get('OUTLOOK_CLIENT_ID'),
    consumer_secret=os.environ.get('OUTLOOK_CLIENT_SECRET'),
    request_token_params={
        'scope': 'https://graph.microsoft.com/Calendars.Read',
    },
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
)

@app.route('/')
def index():
    return 'Welcome to the Family Sports Schedule Notification System!'

@app.route('/login/outlook')
def login_outlook():
    return outlook.authorize(callback=url_for('authorized_outlook', _external=True))

@app.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('authorized_google', _external=True))

@app.route('/login/authorized/google')
def authorized_google():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')  # Save token in session
    return redirect(url_for('fetch_google_events'))  # Redirect to fetch events


@app.route('/login/authorized/outlook')
def authorized_outlook():
    resp = outlook.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['outlook_token'] = (resp['access_token'], '')  # Save token in session
    return redirect(url_for('fetch_outlook_events'))  # Redirect to fetch events

app.secret_key = os.environ.get('FLASK_SECRET_KEY')  # Use the environment variable for your secret key
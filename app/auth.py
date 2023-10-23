from flask import Blueprint, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
import os

# Create a Blueprint
auth = Blueprint('auth', __name__)

# Instantiate the OAuth object
oauth = OAuth()

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


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


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


@outlook.tokengetter
def get_outlook_oauth_token():
    return session.get('outlook_token')


@auth.route('/')
def index():
    return 'Welcome to the Family Sports Schedule Notification System!'


@auth.route('/login_outlook')
def login_outlook():
    return outlook.authorize(callback=url_for('auth.authorized_outlook', _external=True))


@auth.route('/login_google')
def login_google():
    return google.authorize(callback=url_for('auth.authorized_google', _external=True))


@auth.route('/login/authorized/google')
def authorized_google():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    # Save both the access token and the refresh token in the session
    session['google_token'] = (resp['access_token'], resp.get('refresh_token', ''))

    return redirect(url_for('calendar_integration.fetch_google_events'))  # Redirect to fetch events



@auth.route('/login/authorized/outlook')
def authorized_outlook():
    resp = outlook.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['outlook_token'] = (resp['access_token'], '')  # Save token in session
    return redirect(url_for('calendar_integration.fetch_outlook_events'))  # Redirect to fetch events

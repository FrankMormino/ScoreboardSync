from twilio.rest import Client
from flask import Flask

app = Flask(__name__)

# Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

def send_sms(to, message):
    client.messages.create(
        body=message,
        from_='+1234567890',  # Your Twilio phone number
        to=to
    )

@app.route('/send_notifications')
def send_notifications():
    # Fetch filtered events and user notification preferences from your data store
    # ...

    # Loop through each user and send notifications based on their preferences
    for user in users:
        if user.sms_notifications:
            send_sms(user.phone_number, 'Your sports event notifications for today...')
    return 'Notifications sent!'

if __name__ == '__main__':
    app.run()

# File: app/forms.py
from wtforms import Form, BooleanField, StringField, validators

class LinkCalendarForm(Form):
    # Define the fields and validation for your Link Calendar form
    pass

class NotificationConfigForm(Form):
    sms_notifications = BooleanField('Receive SMS Notifications')
    email_notifications = BooleanField('Receive Email Notifications')
    notification_keywords = StringField('Notification Keywords', [validators.Length(min=3)])

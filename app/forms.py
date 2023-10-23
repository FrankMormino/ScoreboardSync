# File: app/forms.py

# Importing necessary classes and modules for form creation and validation
from flask_wtf import FlaskForm  # Importing FlaskForm class from flask_wtf module for creating forms
from wtforms import BooleanField, StringField, SubmitField  # Importing field classes from wtforms module
from wtforms.validators import DataRequired, Length  # Importing validators from wtforms.validators module


# Defining a form for linking calendars
class LinkCalendarForm(FlaskForm):
    # Defining a StringField for calendar URL with a DataRequired validator to ensure the field is not left empty
    calendar_url = StringField('Calendar URL', validators=[DataRequired()])
    # Defining a SubmitField for the submit button with label 'Link Calendar'
    submit = SubmitField('Link Calendar')


# Defining a form for configuring notifications
class NotificationConfigForm(FlaskForm):
    # Defining a BooleanField for opting in/out of SMS notifications
    sms_notifications = BooleanField('Receive SMS Notifications')
    # Defining a BooleanField for opting in/out of Email notifications
    email_notifications = BooleanField('Receive Email Notifications')
    # Defining a StringField for entering notification keywords with a Length validator to ensure a minimum length of
    # 3 characters
    notification_keywords = StringField('Notification Keywords', validators=[Length(min=3)])
    # Defining a SubmitField for the submit button with label 'Save Configuration'
    submit = SubmitField('Save Configuration')

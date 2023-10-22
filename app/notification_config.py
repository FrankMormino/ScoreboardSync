from flask import Flask, render_template, request
from wtforms import Form, BooleanField, StringField, validators

app = Flask(__name__)

class NotificationConfigForm(Form):
    sms_notifications = BooleanField('Receive SMS Notifications')
    email_notifications = BooleanField('Receive Email Notifications')
    notification_keywords = StringField('Notification Keywords', [validators.Length(min=3)])

@app.route('/notification_config', methods=['GET', 'POST'])
def notification_config():
    form = NotificationConfigForm(request.form)
    if request.method == 'POST' and form.validate():
        # Save the form data to the database or other persistent storage
        # ...
        return 'Configuration saved!'
    return render_template('notification_config.html', form=form)

if __name__ == '__main__':
    app.run()

import os
import logging
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, jsonify,
    send_from_directory
)
from app.calendar_integration import calendar_integration  # Import the calendar_integration Blueprint
from app.forms import LinkCalendarForm, NotificationConfigForm
from app.auth import auth

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(calendar_integration, url_prefix='/calendar_integration')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/link_calendar', methods=['GET', 'POST'])
def link_calendar():
    form = LinkCalendarForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Calendar linked successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('link_calendar.html', form=form)


@app.route('/notification_config', methods=['GET', 'POST'])
def notification_config():
    form = NotificationConfigForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Configuration saved successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('notification_config.html', form=form)


@app.route('/view_schedule')
def view_schedule():
    # Assume get_schedule is a function that fetches the schedule from your data store
    schedule = get_schedule()
    return render_template('view_schedule.html', schedule=schedule)


@app.route('/api/events', methods=['GET'])
def api_events():
    # Assume get_events is a function that fetches events from your data store
    events = get_events()
    return jsonify(events)


@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory('static', filename)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)

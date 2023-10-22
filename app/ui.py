from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/link_calendar', methods=['GET', 'POST'])
def link_calendar():
    if request.method == 'POST':
        # Process the submitted form data
        # ...
        return redirect(url_for('home'))
    return render_template('link_calendar.html')

@app.route('/notification_config', methods=['GET', 'POST'])
def notification_config():
    if request.method == 'POST':
        # Process the submitted form data
        # ...
        return redirect(url_for('home'))
    return render_template('notification_config.html')

@app.route('/view_schedule')
def view_schedule():
    # Fetch the synchronized sports schedule from your data store
    # ...
    return render_template('view_schedule.html', schedule=schedule)

if __name__ == '__main__':
    app.run()

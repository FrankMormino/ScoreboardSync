from flask import Flask
from flask import render_template

# Initialize the Flask application
app = Flask(__name__)

# Import the modules
from app import auth
from app import calendar_integration
from app import data_synchronization
from app import event_filtering
from app import notification_config
from app import notification_dispatch
from app import ui

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

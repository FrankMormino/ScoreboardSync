from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

app = Flask(__name__)
scheduler = BackgroundScheduler()

def synchronize_data():
    # Call your functions to fetch data from Google and Outlook
    # You might want to save this data to a database or send it to a Kafka topic
    fetch_google_events()
    fetch_outlook_events()

# Schedule the synchronize_data function to run every hour
scheduler.add_job(synchronize_data, 'interval', hours=1)
scheduler.start()

if __name__ == '__main__':
    app.run()

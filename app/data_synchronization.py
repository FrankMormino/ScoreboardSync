import json
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from app.calendar_integration import fetch_google_events, fetch_outlook_events
import pymongo

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MongoDB connection setup
mongo_client = pymongo.MongoClient("mongodb://alenza:Thisis4devops@localhost:27017/")
mongo_db = mongo_client["calendar_db"]
mongo_collection = mongo_db["events"]

scheduler = BackgroundScheduler()


def batch_insert_update(events):
    bulk_operations = []
    for event in events:
        iCalUID = event.get('iCalUID', '')

        existing_event = mongo_collection.find_one({"iCalUID": iCalUID})
        if existing_event:
            event.pop('_id', None)
            existing_event.pop('_id', None)

            existing_event_str = json.dumps(existing_event, sort_keys=True, default=str)
            event_str = json.dumps(event, sort_keys=True, default=str)

            if existing_event_str != event_str:
                logger.debug(f"Updating event in MongoDB: {event}")
                bulk_operations.append(pymongo.UpdateOne({"iCalUID": iCalUID}, {"$set": event}))
            else:
                logger.debug(f"Event data is the same; skipping update for: {event}")
        else:
            logger.debug(f"Inserting event into MongoDB: {event}")
            bulk_operations.append(pymongo.InsertOne(event))

    if bulk_operations:
        mongo_collection.bulk_write(bulk_operations, ordered=False)


def remove_from_db(events_to_remove):
    try:
        logger.debug("Removing events from MongoDB...")
        if not events_to_remove:
            return

        # Collect iCalUIDs to remove
        iCalUIDs_to_remove = [event['iCalUID'] for event in events_to_remove]

        # Remove events from the database
        mongo_collection.delete_many({"iCalUID": {"$in": iCalUIDs_to_remove}})

        logger.debug("Events removed from MongoDB:")
        for removed_event in events_to_remove:
            logger.debug(removed_event)
    except Exception as e:
        logger.error(f"Error while removing events from MongoDB: {str(e)}")


def save_to_db(events):
    try:
        logger.debug("Saving events to MongoDB...")
        batch_size = 100  # Adjust the batch size as needed
        for i in range(0, len(events), batch_size):
            batch = events[i:i + batch_size]
            batch_insert_update(batch)

        # Remove events that are not in the fetched data
        existing_iCalUIDs = set(event['iCalUID'] for event in events)
        existing_events = list(mongo_collection.find({"iCalUID": {"$nin": list(existing_iCalUIDs)}}))

        remove_from_db(existing_events)  # Remove events not in fetched data

        logger.debug("Events saved to MongoDB successfully.")
    except Exception as e:
        logger.error(f"Error while saving events to MongoDB: {str(e)}")


def synchronize_data():
    try:
        google_events_json = fetch_google_events()
        outlook_events_json = fetch_outlook_events()

        google_events = json.loads(google_events_json)
        outlook_events = json.loads(outlook_events_json)

        all_events = google_events + outlook_events
        save_to_db(all_events)  # Save the events to the database
    except Exception as e:
        logger.error(f"Error while synchronizing data: {str(e)}")


# Schedule the synchronize_data function to run every hour
scheduler.add_job(synchronize_data, 'interval', minutes=2)  # Change to hours=1 for production
scheduler.start()

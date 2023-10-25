import json
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from app.calendar_integration import fetch_google_events, fetch_outlook_events
import pymongo

import uuid


# MongoDB connection setup
mongo_client = pymongo.MongoClient("mongodb://alenza:Thisis4devops@localhost:27017/")
mongo_db = mongo_client["calendar_db"]
mongo_collection = mongo_db["events"]

scheduler = BackgroundScheduler()


def save_to_db(events):
    try:
        client = pymongo.MongoClient("mongodb://alenza:Thisis4devops@localhost:27017/")
        db = client["calendar_db"]
        mongo_collection = db["events"]

        # Create a set to store the iCalUID of events in the new data
        new_event_ids = set() # This is a set of unique values

        for event in events:
            # Log the id value of all events
            print(f"Event id value: {event.get('id')}")

            # Check for a None or null id value
            event_id = event.get('id')
            if event_id is None or event_id.lower() in ["null", "none"]:
                print(f"Skipping event with None or null id value: {event}")
                continue

            # Use iCalUID as a unique identifier for events
            iCalUID = event.get('iCalUID', '')

            # Check if an event with the same iCalUID already exists in the database
            existing_event = mongo_collection.find_one({"iCalUID": iCalUID})

            if existing_event:
                # Remove the '_id' field for comparison
                event.pop('_id', None)
                existing_event.pop('_id', None)

                # Normalize JSON strings for comparison (removes extra spaces)
                existing_event_str = json.dumps(existing_event, sort_keys=True, default=str)
                event_str = json.dumps(event, sort_keys=True, default=str)

                if existing_event_str != event_str:
                    # Update the existing event
                    print(f"Updating event in MongoDB: {event}")
                    mongo_collection.update_one({"iCalUID": iCalUID}, {"$set": event})
                else:
                    print(f"Event data is the same; skipping update for: {event}")
            else:
                # Insert the new event
                print(f"Inserting event into MongoDB: {event}")
                mongo_collection.insert_one(event)

            # Add the iCalUID to the set of new event IDs
            new_event_ids.add(iCalUID)

        # Remove events in MongoDB that are not in the new data
        mongo_collection.delete_many({"iCalUID": {"$nin": list(new_event_ids)}})

    except Exception as e:
        print(f"Error while saving events to MongoDB: {str(e)}")
    finally:
        client.close()




def synchronize_data():
    try:
        # Fetch Google and Outlook events separately
        google_events_json = fetch_google_events()
        outlook_events_json = fetch_outlook_events()

        google_events = json.loads(google_events_json)
        outlook_events = json.loads(outlook_events_json)

        # Save Google events to the database
        save_to_db(google_events)

        # Save Outlook events to the database
        save_to_db(outlook_events)

    except Exception as e:
        print(f"Error while synchronizing data: {str(e)}")

# Schedule the synchronize_data function to run every 5 seconds
scheduler.add_job(synchronize_data, 'interval', minutes=5)
scheduler.start()

from pymongo import MongoClient, ASCENDING
import os

# Load environment variables
MONGO_USER = os.environ.get('MONGO_USER', 'alenza')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'Thisis4devops')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'calendar_db')

# Connect to MongoDB
client = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:27017/{MONGO_DB_NAME}')

# Get the database
db = client[MONGO_DB_NAME]

# Create a collection called 'events'
events_collection = db['events']

# Create an index on the 'id' field
events_collection.create_index([('id', ASCENDING)], unique=True)

print('Setup completed successfully.')

# Optionally, close the connection to MongoDB
client.close()

import os
import shutil
import json
import random
import string
import datetime
from ics import Calendar, Event


# Define a function to move files to the 'old_tests' directory with timestamped subdirectories
def move_old_files():
    # Check if the 'old_tests' directory exists, create it if it doesn't
    if not os.path.exists('old_tests'):
        os.mkdir('old_tests')

    # Get the current timestamp in a format compatible with Windows file naming
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")

    # Create a subdirectory with the timestamp
    subdirectory = os.path.join('old_tests', timestamp)

    # Create the subdirectory if it doesn't exist
    if not os.path.exists(subdirectory):
        os.mkdir(subdirectory)

    # Move the existing 'calendar_events.json' and 'calendar_events.ics' files, if they exist
    for filename in ['calendar_events.json', 'calendar_events.ics']:
        if os.path.exists(filename):
            shutil.move(filename, os.path.join(subdirectory, filename))

    # Print the contents of the current directory
    print("Contents of current directory:")
    for item in os.listdir():
        print(item)

    # Print the contents of the newly created directory
    print(f"Contents of {subdirectory}:")
    for item in os.listdir(subdirectory):
        print(item)


# Check for and move existing files
move_old_files()


# Function to generate a random email address
def generate_email():
    name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    domain = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{name}@{domain}.com"


# Function to generate a random event
def generate_event():
    names = ["Adelina", "Andrew", "Avery", "Dominic", "Frankie", "Joey", "Kalee", "Mackenzie"]
    sports = ["⚾ baseball", "🏀 basketball", "🥎 softball", "⚽ soccer", "🏈 football",
              "🏒 hockey", "🎾 tennis", "🏐 volleyball"]
    event_types = ["Camp", "Clinic", "Game", "Match", "Practice", "Scrimmage", "Tournament", "Tryout"]

    random_name = random.choice(names)
    random_sport = random.choice(sports)
    random_event_type = random.choice(event_types)

    # Extract the emoji and sport name
    emoji = random_sport.split()[0]
    sport_name = ' '.join(random_sport.split()[1:])

    locations = {
        "basketball": "Toms River East Little League, 2195 Windsor Ave, Toms River, NJ 08753, USA",
        "baseball": "Brick American Baseball League, 2000 Lanes Mill Rd, Brick Township, NJ 08724, USA",
        "soccer": "Soccer Field, 123 Main St, Sample City, NJ 12345, USA",
        "softball": "Drum Point Sports Complex, Brick Blvd, Brick Township, NJ 08723, USA",
        "volleyball": "Lake Riviera Middle School, 171 Beaverson Blvd, Brick Township, NJ 08723, USA",
        "football": "Football Stadium, 456 Stadium Dr, Stadium City, NJ 54321, USA",
        "hockey": "Hockey Arena, 789 Ice Rink Rd, Ice City, NJ 67890, USA",
        "tennis": "Tennis Court, 101 Racket St, Racketville, NJ 13579, USA"
    }

    random_location = locations.get(sport_name, "Default Location")

    # Calculate a random number of days (between 1 and 5) to schedule the event in the future
    random_days = random.randint(1, 5)

    # Calculate a random number of minutes (between 0 and 1440) to add to the start time
    random_minutes = random.randint(0, 1440)

    # Calculate the end time by adding 1 to 2 hours (60 to 120 minutes) to the start time
    end_minutes = random_minutes + random.randint(60, 120)

    # Format the start and end times in ISO 8601 format
    start_time = (datetime.datetime.now() + datetime.timedelta(days=random_days, minutes=random_minutes)).isoformat()
    end_time = (datetime.datetime.now() + datetime.timedelta(days=random_days, minutes=end_minutes)).isoformat()

    # Calculate the emoji character for the sport
    emoji = random_sport.split()[0]

    # Format the "summary" field with emoji as Unicode characters
    summary = f"{random_name} {emoji} {random_event_type} {sport_name}"

    # Set the "created" field to the current date and time
    created_time = datetime.datetime.now().isoformat()

    event_data = {
        "kind": "calendar#event",
        "etag": ''.join(random.choice(string.digits) for _ in range(16)),
        "id": f"event-id-{random.randint(1, 9999)}",
        "status": "confirmed",
        "htmlLink": f"https://www.google.com/calendar/event?eid=event-id-{random.randint(1, 9999)}",
        "created": created_time,  # Set "created" to the current date and time
        "updated": created_time,  # Set "updated" to the current date and time
        "summary": summary,
        "location": random_location,
        "creator": {"email": generate_email(), "self": True},
        "organizer": {"email": generate_email(), "self": True},
        "start": {"dateTime": start_time, "timeZone": "America/New_York"},
        "end": {"dateTime": end_time, "timeZone": "America/New_York"},
        "iCalUID": f"event-id-{random.randint(1, 9999)}@google.com",
        "sequence": 0,
        "reminders": {"useDefault": True},
        "eventType": "default"
    }

    return event_data


# Ask for the number of events
num_events = int(input("Enter the number of events you'd like to create: "))

# Create a list to hold the events
events = []

# Create a Calendar object to hold the events for the ICS file
cal = Calendar()

# Generate the specified number of events
for _ in range(num_events):
    event = generate_event()  # Generate an event
    events.append(event)  # Add it to the events list

    # Create an Event object for the ICS file and populate it with data
    ics_event = Event()
    ics_event.uid = event["iCalUID"]
    ics_event.name = event["summary"]
    ics_event.begin = event["start"]["dateTime"]
    ics_event.end = event["end"]["dateTime"]
    ics_event.location = event["location"]

    # Add the event to the calendar
    cal.events.add(ics_event)

# Save the events to a JSON file
with open('calendar_events.json', 'w') as json_file:
    json.dump(events, json_file, indent=2)

# Save the calendar to an ICS file
with open('calendar_events.ics', 'w', encoding='utf-8') as ics_file:
    ics_file.writelines(cal)

print("Events have been generated and saved to calendar_events.json and calendar_events.ics.")

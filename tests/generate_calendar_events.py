import json
import random
import string
import datetime


# Function to generate a random email address
def generate_email():
    name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    domain = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{name}@{domain}.com"


# Function to generate a random event
def generate_event():
    names = ["Andrew", "Frankie", "Dominic", "Adelina", "Mackenzie", "Kalee", "Avery", "Joey", "Olivia", "Emma"]
    sports = ["🏀 basketball", "⚾ baseball", "⚽ soccer", "🥎 softball", "🏐 volleyball", "🏈 football", "🏒 hockey",
              "🎾 tennis"]
    event_types = ["Practice", "Game", "Match", "Scrimmage", "Tournament", "Clinic", "Camp", "Tryout"]

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

    event_data = {
        "kind": "calendar#event",
        "etag": ''.join(random.choice(string.digits) for _ in range(16)),
        "id": f"event-id-{random.randint(1, 9999)}",
        "status": "confirmed",
        "htmlLink": f"https://www.google.com/calendar/event?eid=event-id-{random.randint(1, 9999)}",
        "created": datetime.datetime.now().isoformat(),
        "updated": datetime.datetime.now().isoformat(),
        "summary": f"{random_name} {emoji} {random_event_type} {sport_name}",
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

# Generate the specified number of events
for _ in range(num_events):
    event = generate_event()  # Generate an event
    events.append(event)  # Add it to the events list

# Save the events to a JSON file
with open('calendar_events.json', 'w') as json_file:
    json.dump(events, json_file, indent=2)

print("Events have been generated and saved to calendar_events.json.")

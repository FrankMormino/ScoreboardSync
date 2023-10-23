#!/bin/bash

# Function to generate a random email address
function generate_email() {
  local name
  local domain
  name=$(cat /dev/urandom | tr -dc 'a-zA-Z' | fold -w 8 | head -n 1)
  domain=$(cat /dev/urandom | tr -dc 'a-z' | fold -w 8 | head -n 1)
  echo "$name@$domain.com"
}

# Function to generate a random event
function generate_event() {
  local name
  local sport
  local event_type
  name=("Andrew" "Frankie" "Dominic" "Adelina" "Mackenzie" "Kalee" "Avery" "Joey" "Olivia" "Emma")
  sport=("basketball" "baseball" "soccer" "softball" "volleyball" "football" "hockey" "tennis")
  event_type=("Practice" "Game")

  local random_name
  local random_sport
  local random_event_type
  local random_location

  random_name=${name[$RANDOM % ${#name[@]}]}
  random_sport=${sport[$RANDOM % ${#sport[@]}]}
  random_event_type=${event_type[$RANDOM % ${#event_type[@]}]}

  case "$random_sport" in
    "basketball")
      random_location="Toms River East Little League, 2195 Windsor Ave, Toms River, NJ 08753, USA"
      ;;
    "baseball")
      random_location="Brick American Baseball League, 2000 Lanes Mill Rd, Brick Township, NJ 08724, USA"
      ;;
    "soccer")
      random_location="Soccer Field, 123 Main St, Sample City, NJ 12345, USA"
      ;;
    "softball")
      random_location="Drum Point Sports Complex, Brick Blvd, Brick Township, NJ 08723, USA"
      ;;
    "volleyball")
      random_location="Lake Riviera Middle School, 171 Beaverson Blvd, Brick Township, NJ 08723, USA"
      ;;
    *)
      random_location="Toms River East Little League, 2195 Windsor Ave, Toms River, NJ 08753, USA"
      ;;
  esac

  echo "{\"kind\":\"calendar#event\",\"etag\":\"$(cat /dev/urandom | tr -dc '0-9' | fold -w 16 | head -n 1)\",\"id\":\"event-id-$RANDOM\",\"status\":\"confirmed\",\"htmlLink\":\"https://www.google.com/calendar/event?eid=event-id-$RANDOM\",\"created\":\"$(date -Iseconds)\",\"updated\":\"$(date -Iseconds)\",\"summary\":\"$random_name 🏈 $random_sport $random_event_type\",\"location\":\"$random_location\",\"creator\":{\"email\":\"$(generate_email)\",\"self\":true},\"organizer\":{\"email\":\"$(generate_email)\",\"self\":true},\"start\":{\"dateTime\":\"2023-10-$(shuf -i 24-28 -n 1)T$(shuf -i 10-19 -n 1):00:00-04:00\",\"timeZone\":\"America/New_York\"},\"end\":{\"dateTime\":\"2023-10-$(shuf -i 24-28 -n 1)T$(shuf -i 10-19 -n 1):00:00-04:00\",\"timeZone\":\"America/New_York\"},\"iCalUID\":\"event-id-$RANDOM@google.com\",\"sequence\":0,\"reminders\":{\"useDefault\":true},\"eventType\":\"default\"},"
}

# Ask for the number of events
read -p "Enter the number of events you'd like to create: " num_events

# Ask whether to use random organizers
read -p "Do you want to use random organizers (yes/no)? " use_random_organizers

# Create an array to hold the events
events=()

# Generate the specified number of events
for ((i = 1; i <= num_events; i++)); do
  events+=("$(generate_event)")
done

# Save the events to a JSON file
echo "[" >>calendar_events.json
echo "${events[@]}" >>calendar_events.json
echo "]" >>calendar_events.json

echo "Events have been generated and saved to calendar_events.json."


#!/bin/bash

# Function to generate a random email address
function generate_email() {
  local name
  local domain
  name=$(cat /dev/urandom | tr -dc 'a-zA-Z' | fold -w 8 | head -n 1)
  domain=$(cat /dev/urandom | tr -dc 'a-z' | fold -w 8 | head -n 1)
  #name=$(head -c 8 /dev/urandom | tr -dc 'a-zA-Z')
  #domain=$(head -c 8 /dev/urandom | tr -dc '[:lower:]')


  echo "$name@$domain.com"
}

# Function to generate a random event
function generate_event() {
  local name
  local sport
  local event_type
  name=("Andrew" "Frankie" "Dominic" "Adelina" "Mackenzie" "Kalee" "Avery" "Joey" "Olivia" "Emma")
  sport=("🏀 basketball" "⚾ baseball" "⚽ soccer" "🥎 softball" "🏐 volleyball" "🏈 football" "🏒 hockey" "🎾 tennis")
  event_type=("Practice" "Game" "Match" "Scrimmage" "Tournament" "Clinic" "Camp" "Tryout")

  local random_name
  local random_sport
  local random_event_type
  local random_location  # Move the location inside the function

  random_name=${name[$RANDOM % ${#name[@]}]}
  random_sport=${sport[$RANDOM % ${#sport[@]}]}
  random_event_type=${event_type[$RANDOM % ${#event_type[@]}]}

  # Extract the emoji and sport name
  emoji=$(echo "$random_sport" | cut -d' ' -f1)
  sport_name=$(echo "$random_sport" | cut -d' ' -f2-)

  case "$sport_name" in
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
    "football")
      random_location="Football Stadium, 456 Stadium Dr, Stadium City, NJ 54321, USA"
      ;;
    "hockey")
      random_location="Hockey Arena, 789 Ice Rink Rd, Ice City, NJ 67890, USA"
      ;;
    "tennis")
      random_location="Tennis Court, 101 Racket St, Racketville, NJ 13579, USA"
      ;;
    *)
      random_location="Default Location"
      ;;
  esac

  #echo "{\"kind\":\"calendar#event\",\"etag\":\"$(cat /dev/urandom | tr -dc '0-9' | fold -w 16 | head -n 1)\",\"id\":\"event-id-$RANDOM\",\"status\":\"confirmed\",\"htmlLink\":\"https://www.google.com/calendar/event?eid=event-id-$RANDOM\",\"created\":\"$(date -Iseconds)\",\"updated\":\"$(date -Iseconds)\",\"summary\":\"$random_name $emoji $random_event_type $sport_name\",\"location\":\"$random_location\",\"creator\":{\"email\":\"$(generate_email)\",\"self\":true},\"organizer\":{\"email\":\"$(generate_email)\",\"self\":true},\"start\":{\"dateTime\":\"2023-10-$(shuf -i 24-28 -n 1)T$(shuf -i 10-19 -n 1):00:00-04:00\",\"timeZone\":\"America/New_York\"},\"end\":{\"dateTime\":\"2023-10-$(shuf -i 24-28 -n 1)T$(shuf -i 10-19 -n 1):00:00-04:00\",\"timeZone\":\"America/New_York\"},\"iCalUID\":\"event-id-$RANDOM@google.com\",\"sequence":0,\"reminders\":{\"useDefault\":true},\"eventType\":\"default\"},"
  echo "{\"kind\":\"calendar#event\",\"etag\":\"$(cat /dev/urandom | tr -dc '0-9' | fold -w 16 | head -n 1)\",\"id\":\"event-id-\$RANDOM\",\"status\":\"confirmed\",\"htmlLink\":\"https://www.google.com/calendar/event?eid=event-id-\$RANDOM\",\"created\":\"$(date -Iseconds)\",\"updated\":\"$(date -Iseconds)\",\"summary\":\"$random_name $emoji $random_event_type $sport_name\",\"location\":\"$random_location\",\"creator\":{\"email\":\"$(generate_email)\",\"self\":true},\"organizer\":{\"email\":\"$(generate_email)\",\"self\":true},\"start\":{\"dateTime\":\"2023-10-\$(shuf -i 24-28 -n 1)T\$(shuf -i 10-19 -n 1):00:00-04:00\",\"timeZone\":\"America/New_York\"},\"end\":{\"dateTime\":\"2023-10-\$(shuf -i 24-28 -n 1)T\$(shuf -i 10-19 -n 1):00:00-04:00\",\"timeZone\":\"America/New_York\"},\"iCalUID\":\"event-id-\$RANDOM@google.com\",\"sequence\":0,\"reminders\":{\"useDefault\":true},\"eventType\":\"default\"},"
}


# Ask for the number of events
read -r -p "Enter the number of events you'd like to create: " num_events

# Create an array to hold the events
events=()

# Generate the specified number of events
for ((i = 1; i <= num_events; i++)); do
  event=$(generate_event)  # Generate an event
  events+=("$event")       # Add it to the events array
done

# Save the events to a JSON file
echo "[" >>calendar_events.json
# Consider using { cmd1; cmd2; } >> file instead of individual redirects.
echo "${events[@]}" | sed "s/,$//" >>calendar_events.json  # Remove trailing comma
echo "]" >>calendar_events.json


echo "Events have been generated and saved to calendar_events.json."


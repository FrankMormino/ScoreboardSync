#!/bin/bash

# Function to generate a random email address
generate_random_email() {
  local random_name=$(tr -dc 'a-zA-Z' < /dev/urandom | fold -w 8 | head -n 1)
  local random_domain=$(tr -dc 'a-z' < /dev/urandom | fold -w 8 | head -n 1).com
  echo "${random_name}@${random_domain}"
}

# Function to generate a random kids' name
generate_kids_name() {
  local kids_names=("Andrew" "Frankie" "Dominic" "Adelina" "Mackenzie" "Kalee" "Avery" "Joey" "Olivia" "Emma" "Liam" "Aiden" "Sophia" "Ella" "Mia" "Lucas" "Ethan" "Ava" "Noah" "Isabella")
  echo "${kids_names[$((RANDOM % ${#kids_names[@]}))]}"
}

# Function to generate a random sports item
generate_sports_item() {
  local sports_items=("baseball" "football" "soccerball" "softball" "volleyball" "basketball")
  echo "${sports_items[$((RANDOM % ${#sports_items[@]}))]}"
}

# Prompt for the number of events
read -p "Enter the number of events you'd like to create: " num_events

# Check if input is a valid number
if [[ ! $num_events =~ ^[0-9]+$ ]]; then
  echo "Invalid input. Please enter a valid number."
  exit 1
fi

# Ask if random organizers should be used
read -p "Do you want to use random organizers (yes/no)? " use_random_organizers

# Create a JSON file to store the events
output_file="calendar_events.json"
echo "[" > "$output_file"

# Generate random events
for ((i = 1; i <= num_events; i++)); do
  event_id="event-id-$i"
  etag="\"$(shuf -i 1000000000000000-9999999999999999 -n 1)\""
  html_link="\"https://www.google.com/calendar/event?eid=${event_id}\""
  created="\"$(date -Iseconds -u)\""
  updated="$created"
  kids_name=$(generate_kids_name)
  sports_item=$(generate_sports_item)
  summary="\"$kids_name 🏈 $sports_item $(if [ $((RANDOM % 2)) -eq 0 ]; then echo "Game"; else echo "Practice"; fi)\""
  start="\"$(date -Iseconds -u -d "+${i} days")\""
  end="\"$(date -Iseconds -u -d "+${i} days 1 hour")\""

  if [ "$use_random_organizers" = "yes" ]; then
    organizer_email=$(generate_random_email)
  else
    read -p "Enter the organizer's email for Event $i: " organizer_email
  fi

  cat <<EOF >> "$output_file"
  {
    "kind": "calendar#event",
    "etag": $etag,
    "id": "$event_id",
    "status": "confirmed",
    "htmlLink": $html_link,
    "created": $created,
    "updated": $updated,
    "summary": $summary,
    "creator": {
      "email": "$organizer_email",
      "self": true
    },
    "organizer": {
      "email": "$organizer_email",
      "self": true
    },
    "start": {
      "dateTime": $start,
      "timeZone": "America/New_York"
    },
    "end": {
      "dateTime": $end,
      "timeZone": "America/New_York"
    }
  },
EOF

done

# Remove the trailing comma from the last event
sed -i '$s/,$//' "$output_file"

# Close the JSON array
echo "]" >> "$output_file"

echo "Events have been generated and saved to $output_file."


#!/bin/bash

# Directories
mkdir -p app/templates
mkdir -p app/static/css
mkdir -p app/static/js
mkdir -p app/static/img
mkdir -p tests/test_data

# Python Modules
touch app/__init__.py
touch app/auth.py
touch app/calendar_integration.py
touch app/data_synchronization.py
touch app/event_filtering.py
touch app/notification_config.py
touch app/notification_dispatch.py
touch app/ui.py

# HTML Templates
touch app/templates/index.html
touch app/templates/link_calendar.html
touch app/templates/notification_config.html
touch app/templates/view_schedule.html

# Test Scripts
touch tests/test_auth.py
touch tests/test_calendar_integration.py

# Docker and Dependency files
touch Dockerfile
touch docker-compose.yml
touch requirements.txt

echo "Directory structure and files have been created."


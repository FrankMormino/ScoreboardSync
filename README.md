# ScoreboardSync

ScoreboardSync is a family sports schedule notification system, designed to help families stay updated on their kids' sports schedules. This project is structured as a Flask application, with several modules to handle authentication, calendar integration, data synchronization, event filtering, and notifications.

## Directory Structure

- **app/**: Main application directory containing Python modules and templates.
- **app/templates/**: Contains HTML templates for the user interface.
- **app/static/**: Holds static files like CSS, JavaScript, and images.
- **tests/**: Directory for test scripts and test data.
- **Dockerfile**: Defines how to build the Docker image for this project.
- **docker-compose.yml**: Used by Docker Compose to define and manage multi-container Docker applications.
- **requirements.txt**: Lists all the Python dependencies required by this project.

## Setup Instructions

1. **Clone the Repository**:
```bash
git clone https://github.com/FrankMormino/ScoreboardSync.git
cd ScoreboardSync
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Build the Docker Image**:
```bash
docker build -t scoreboardsync .
```

4. **Run the Application with Docker Compose**:
```bash
docker-compose up
```

## Usage

1. **Linking Calendars**:
   - Navigate to `http://localhost:5000/link_calendar` to link your Google or Outlook calendar.

2. **Configuring Notifications**:
   - Go to `http://localhost:5000/notification_config` to set your notification preferences.

3. **Viewing Schedule**:
   - Access `http://localhost:5000/view_schedule` to view the synchronized sports schedule.

4. **Sending Notifications**:
   - Notifications will be sent based on the preferences set in the Notification Configuration.

## Testing

- Run the test scripts located in the `tests` directory to verify the functionality of each module.

## Deployment

- This application is prepared for deployment as Docker containers, making it easy to deploy on any system or cloud platform that supports Docker.

## Contributing

- Feel free to fork this repository, and submit pull requests for any enhancements or bug fixes.

## License

- This project is open-source, under the MIT License.

## Contact

- For any inquiries or contributions, please contact Frank Mormino.


In this updated `README.md`:

- I've added a brief introduction to `ScoreboardSync`.
- Provided clear setup instructions for cloning the repository, installing dependencies, building the Docker image, and running the application with Docker Compose.
- Included a simple usage section to explain how to link calendars, configure notifications, view the schedule, and understand how notifications are sent.
- Added a section for testing, deployment, contributing, licensing, and contact information.
- Used Markdown formatting to organize the content for better readability.

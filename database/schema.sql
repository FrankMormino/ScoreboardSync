CREATE DATABASE IF NOT EXISTS calendar_db;
USE calendar_db;

CREATE TABLE IF NOT EXISTS events (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    kind VARCHAR(255),
    etag VARCHAR(255),
    status VARCHAR(255),
    htmlLink VARCHAR(255),
    created DATETIME,
    updated DATETIME,
    summary VARCHAR(255),
    creator_email VARCHAR(255),
    organizer_email VARCHAR(255),
    start_datetime DATETIME,
    end_datetime DATETIME,
    timeZone VARCHAR(255),
    iCalUID VARCHAR(255),
    sequence INT,
    reminders_default BOOLEAN,
    eventType VARCHAR(255)
);


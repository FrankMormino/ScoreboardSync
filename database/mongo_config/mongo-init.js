db = db.getSiblingDB('calendar_db');

db.createUser(
  {
    user: 'alenza',
    pwd: 'Thisis4devops',
    roles: [
      {
        role: 'dbOwner',
        db: 'calendar_db',
      },
    ],
  }
);

// Create a collection named 'events' in the 'calendar_db' database
//db.createCollection('events');

// Optionally, you could insert a document into the 'events' collection to ensure the database is created
// db.events.insert({ test: "document" });

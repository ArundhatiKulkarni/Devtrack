# DevTrack

DevTrack is a Django-based backend API for tracking engineering issues and reporters. It provides REST-style endpoints for creating, retrieving, updating, and deleting reporters, as well as creating and querying engineering issues.

The project uses JSON files for data persistence and demonstrates object-oriented programming concepts such as abstraction, inheritance, and method overriding.

---

## Features

- Reporter management
- Issue management
- JSON-based data storage
- Input validation
- Issue filtering by ID and status
- Object-oriented entity design
- Critical and low-priority issue subclasses
- REST-style API endpoints
- HTTP status code handling

---

## Technologies Used

- Python
- Django
- JSON
- Postman
- Git & GitHub

---

## Project Structure

```text
Devtrack/
│
├── manage.py
├── reporters.json
├── issues.json
├── README.md
│
├── devtrack/
│   ├── settings.py
│   └── urls.py
│
└── issues/
    ├── models.py
    ├── views.py
    └── urls.py
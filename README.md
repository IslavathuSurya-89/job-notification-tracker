# JobTrack — Python Job Notification Tracker

A responsive Flask web app to organize government and private job notifications. Save qualifications, age limits, vacancies, salary details, dates, status, notes, and application URLs in a local SQLite database.

> **Important:** Seed data is fictional demonstration data. It is not a real vacancy announcement. Always verify recruitment details on the official website.

## Features

* Dashboard metrics: saved jobs, open status, upcoming deadlines, and past deadlines
* Add, view, edit, and delete job notifications (CRUD)
* Search by job title, organization, department, or location
* Filter by Government/Private, Open/Closed/Applied status, and qualification
* Store eligibility, vacancies, salary, dates, notes, and official application links
* Responsive layout for desktop and mobile
* SQLite database persistence
* Unit tests for core application flows

## Tech Stack

* Python 3.10+
* Flask
* Flask-SQLAlchemy
* SQLite
* HTML5 and CSS3
* `unittest`

## Project Structure

```text
job-notification-tracker/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   └── job_form.html
└── tests/
    └── test_app.py
```

## Run Locally

### 1. Install Python

Install Python 3.10 or newer from https://www.python.org/downloads/.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Optional: Add sample jobs

```powershell
flask --app app seed
```

Sample records are fictional and are provided for demonstration only.

### 5. Run the application

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser. Stop the server with `Ctrl+C`.

The SQLite database is created automatically on first run.

## Run Tests

```powershell
python -m unittest discover -s tests -v
```

## Suggested Resume Entry

**JobTrack — Job Notification Tracker | Python, Flask, SQLite, HTML, CSS**

* Built a web application to maintain government and private job notifications.
* Implemented CRUD operations, SQLite persistence, search, and filtering.
* Added dashboard metrics for open jobs and application deadlines.
* Created automated unit tests for key application flows.

Only include features you have tested and can explain in an interview.

## Future Improvements

1. Add user login and individual job lists.
2. Export saved jobs to CSV.
3. Add bookmarks and application-status history.
4. Add pagination and date-range filters.
5. Improve form validation and secure configuration.
6. Deploy using a production WSGI server and a persistent database.

## Security Notes

This is a learning project, not a production-hardened application. Before deploying publicly, move `SECRET_KEY` to an environment variable, disable Flask debug mode, add CSRF protection and authentication, validate external URLs, and use a production WSGI server.

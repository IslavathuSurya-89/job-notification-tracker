# JobTrack — Python Job Notification Tracker

A responsive Flask web app to organize government and private job notifications. Save qualifications, age limits, vacancies, salary details, dates, status, notes, and application URLs in a local SQLite database.

> **Important:** Seed data is fictional demonstration data. It is not a real vacancy announcement. Always verify recruitment details on the official website.

## Features

- Dashboard metrics: saved jobs, open status, deadlines in the next seven days, and past deadlines
- Add, view, edit, and delete job notifications (CRUD)
- Search by job title, organization, department, or location
- Filter by Government/Private, Open/Closed/Applied status, and qualification
- Store eligibility, vacancies, salary, dates, notes, and official application links
- Responsive layout for desktop and mobile
- SQLite persistence
- Unit tests for core flows

## Tech stack

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5 and CSS3
- `unittest`

## Project structure

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

## Run locally

### 1. Install Python

Install Python 3.10 or newer from https://www.python.org/downloads/. On Windows, select **Add Python to PATH** during setup.

### 2. Open the project folder and create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. (Optional) Load fictional sample jobs

```bash
flask --app app seed
```

The command adds sample jobs only when the database is empty. These records use `example.com` and are not real job openings.

### 5. Start the app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser. Stop the server with `Ctrl+C`.

The SQLite database is created automatically on first run.

## Run tests

Activate the virtual environment, then run:

```bash
python -m unittest discover -s tests -v
```

Tests cover dashboard loading, creating a job, required fields, search, and deleting a job.

## Upload to GitHub

Create a **new empty repository** on https://github.com/new (for example, `job-notification-tracker`). Do not add a README there because this project already has one.

From the project directory:

```bash
git init
git add .
git commit -m "Build JobTrack Python job notification tracker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/job-notification-tracker.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. GitHub may ask you to authenticate using a browser or credential manager; use the supported sign-in flow, not your account password as a Git password.

If Git is not installed, install it from https://git-scm.com/downloads.

## Suggested resume entry

**JobTrack — Job Notification Tracker | Python, Flask, SQLite, HTML, CSS**
- Built a responsive web application to maintain government and private job notifications.
- Implemented CRUD operations, SQLite persistence, search, and multi-field filtering.
- Added dashboard metrics to highlight open jobs and upcoming or passed deadlines.
- Wrote automated unit tests for key application flows.

Only list technologies and features you have personally run and can explain in an interview.

## Good next improvements

1. Add login and per-user job lists.
2. Export saved jobs to CSV.
3. Add bookmarks and application-status history.
4. Add pagination and date-range filters.
5. Add form validation and secure configuration for production.
6. Deploy with a managed database and production WSGI server.

## Security and deployment notes

This is a learning project, not production-hardened. Before deploying publicly, move `SECRET_KEY` to an environment variable, disable Flask debug mode, add CSRF protection and authentication, validate external URLs, and use a production WSGI server. SQLite is convenient locally; use a persistent database/storage strategy for deployment.

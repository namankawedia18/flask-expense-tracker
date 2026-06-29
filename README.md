# Expense Tracker

A simple Flask-based expense tracker that helps you record, view, search, sort, and analyze your expenses.

## Features

- Add new expenses with name, amount, and date
- View all expenses in a clean dashboard
- Search expenses by name
- Sort expenses by date, amount, or event name
- Filter expenses by date range or quick presets (today, week, month, year)
- See summary statistics such as total spending, transaction count, and category breakdown
- Edit or delete existing expenses

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite

## Project Structure

- app.py - Main Flask application
- templates/ - HTML templates for the UI
- static/ - CSS and static assets
- instance/ - SQLite database location

## Prerequisites

Make sure you have Python installed on your system.

## Installation

1. Clone the repository
2. Navigate to the project folder
3. Create and activate a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the app with:

```bash
python app.py
```

Then open your browser and go to:

```text
http://127.0.0.1:5000/
```

## Usage

- Open the home page to access the app
- Use the Add Expense page to record a new expense
- Visit the expenses page to view and manage your records
- Apply filters, search, and sorting options to analyze your spending

## Notes

The application uses SQLite, so your data will be stored in a local database file created when the app runs.

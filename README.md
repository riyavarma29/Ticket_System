# Support Ticket CRM System

## Project Overview

The Support Ticket CRM System is a web-based customer support management application built using FastAPI, SQLAlchemy, SQLite, Jinja2 Templates, HTML, and Tailwind CSS.

The application allows users to create support tickets, view ticket details, update ticket status, add notes/comments, and filter/search tickets efficiently. The project focuses on providing a clean UI and simple ticket management workflow.

---

# Features

* Create support tickets
* View detailed ticket information
* Update ticket status
* Add notes/comments to tickets
* Search tickets
* Filter tickets by status
* Responsive UI using Tailwind CSS
* Ticket creation timestamp
* Clean and user-friendly dashboard

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite

## Frontend

* HTML
* Tailwind CSS
* Jinja2 Templates

---

# Project Structure

```bash
Ticket_System/
│
├── app/
│   ├── main.py
│   ├── crud.py
│   ├── models.py
│   ├── database.py
│   └── templates/
│       ├── index.html
│       ├── create_ticket.html
│       └── ticket_detail.html
│
├── static/
│
├── requirements.txt
└── tickets.db
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your-github-repo-link>
```

## 2. Navigate to Project Folder

```bash
cd Ticket_System
```

## 3. Create Virtual Environment

```bash
python -m venv venv
```

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

---

# Open in Browser

```bash
http://127.0.0.1:8000
```

---

# Challenges Faced

* Handling FastAPI template rendering errors
* Managing update routes and form submissions
* Integrating SQLAlchemy with FastAPI
* Creating responsive UI using Tailwind CSS
* Debugging Jinja2 template issues

---

# Future Improvements

* User Authentication
* Admin Dashboard
* Email Notifications
* Ticket Priority System
* File Attachments
* Pagination

---

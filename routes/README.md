# Flask Student Management System

## 📌 Overview
This is a Flask-based web application for managing students with authentication, dashboards, and an audit logging system to track user activities such as login, updates, deletions, and additions.

---

## 🚀 Features
- User registration and login system
- Password reset functionality
- Dashboard for managing students
- Add / update / delete student records
- Audit logging system (tracks all actions)
- View audit logs in a table format
- REST API integration with frontend (Fetch API)

---

## 🛠️ Tech Stack
- Python (Flask)
- SQLite (Database)
- HTML, CSS, JavaScript
- Flask Blueprints
- Fetch API

---

## 📂 Project Structure


project/
│
├── routes/
│ ├── auth_route.py
│ ├── student_route.py
│
├── templates/
│ ├── audit.html
│ ├── dashboard.html
│ ├── login.html
│ ├── land.html
│ ├── register.html
│ ├── resetpassword.html
│
├── static/
│ └── js/
│ ├── audit.js
│
├── database.db
├── app.py
└── README.md
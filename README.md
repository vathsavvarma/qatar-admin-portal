# Qatar Foundation Admin Portal (Backend + Integration)

## 🚀 Project Overview

This project is a full-stack Admin Portal built using **Flask (Python)** for the backend and an existing frontend UI.
It includes authentication, secure password reset, and full CRUD operations for managing opportunities.

The system is designed so that:

* Data is stored in a database (SQLite)
* UI updates dynamically without page reload
* Each admin manages only their own data

---

## 🔐 Features

### Authentication

* Admin Signup (with validation & password hashing)
* Admin Login (Flask-Login session management)
* Forgot Password (secure token-based reset link with 1-hour expiry)

### Opportunity Management (CRUD)

* View all opportunities (user-specific)
* Add new opportunity
* View opportunity details
* Edit opportunity (form-based update)
* Delete opportunity

### Frontend Integration

* Fully dynamic UI (no hardcoded data)
* Uses Fetch API to communicate with backend
* Real-time updates without page refresh

---

## 🛠 Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **Authentication:** Flask-Login
* **ORM:** Flask-SQLAlchemy
* **Security:** Werkzeug (password hashing), itsdangerous (token generation)
* **Frontend:** HTML, CSS, JavaScript (provided UI)

---

## 📁 Project Structure

```
qatar_admin_backend/
│
├── app.py
├── models.py
├── routes.py
├── config.py (optional)
├── requirements.txt
│
├── static/
├── templates/
```

---

## ▶️ How to Run the Project

### 1. Clone the repository

```
git clone https://github.com/vathsavvarma/qatar-admin-portal.git
cd qatar_admin_backend
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Initialize Database (IMPORTANT)

Before running the app for the first time, **temporarily add this code in `app.py`:**

```python
with app.app_context():
    db.create_all()
```

Then run:

```
python app.py
```

👉 This will create `database.db`

⚠️ After database is created, **remove this code** from `app.py` to avoid re-running it every time.

---

### 5. Run the application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Forgot Password Flow

* Enter email in UI
* Backend generates a reset token
* Reset link is printed in terminal (no email service)
* Token expires in 1 hour

Example:

```
http://127.0.0.1:5000/reset-password/<token>
```

---

## ⚠️ Important Notes

* Passwords are securely hashed (never stored in plain text)
* All opportunity routes are protected (login required)
* Each user can only access their own data (admin_id check)
* No frontend code was modified (as per assignment requirement)

---

## 📌 Author

**Rudraraju Vathsav Varma**

---

## ✅ Status

✔ Authentication completed
✔ Forgot password (secure token-based) implemented
✔ Full CRUD operations completed
✔ Frontend fully integrated
✔ Assignment requirements fully satisfied

---

## 🎯 Conclusion

This project demonstrates:

* Secure authentication design
* REST API development
* Database modeling with relationships
* Full frontend-backend integration
* Real-world CRUD application architecture

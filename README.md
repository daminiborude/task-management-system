# 🚀 Task Management System API

A secure REST API built using FastAPI, MySQL, SQLAlchemy, and JWT Authentication.

---

# ✨ Features

* User Registration & Login
* JWT Authentication
* Password Hashing with Bcrypt
* Create, Read, Update & Delete Tasks
* Protected APIs
* MySQL Database Integration
* Swagger API Documentation

---

# 🛠️ Tech Stack

* Python
* FastAPI
* MySQL
* SQLAlchemy
* JWT Authentication
* Pydantic
* Uvicorn

---

# ▶️ Steps to Run the Project

## 1️⃣ Clone Repository

```bash
git clone https://github.com/daminiborude/Task-Management-System.git
cd Task-Management-System
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Create MySQL Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE taskdb;
```

---

## 5️⃣ Configure Database

Open:

```bash
app/database.py
```

Update:

```python
DATABASE_URL = "mysql+pymysql://root:password@localhost/taskdb"
```

Replace:

* `root` → your MySQL username
* `password` → your MySQL password

---

## 6️⃣ Run the Server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```bash
http://127.0.0.1:8000
```

---

# 📘 Swagger API Docs

Open in browser:

```bash
http://127.0.0.1:8000/docs
```

---

# 🔐 Authentication Flow

1. Register User → `/register`
2. Login User → `/login`
3. Copy JWT Token
4. Click 🔒 Authorize in Swagger
5. Paste Token
6. Access Protected APIs

---

# ✅ Available APIs

* POST `/register`
* POST `/login`
* POST `/tasks`
* GET `/tasks`
* GET `/tasks/{id}`
* PUT `/tasks/{id}`
* DELETE `/tasks/{id}`

---


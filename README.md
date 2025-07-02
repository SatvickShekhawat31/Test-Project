# Test-Project

## 📦 Test Project – Secure File Sharing System

A Django REST API for secure file sharing between **Ops Users** and **Client Users**.  
Supports registration, login, file upload (only by Ops users), secure download link generation, and profile management.

---

## 🚀 Features
- Register & login for Ops and Client users
- Ops users can upload only `.pptx`, `.docx`, `.xlsx` files
- Clients get encrypted download links for files
- Token-based authentication
- Ready Postman collection for testing

---

## API Endpoints (examples)
- `POST /api/register/`
- `POST /api/login/`
- `GET /api/profile/`
- `POST /api/files/`
- `GET /api/files/`
- `GET /download/<file_id>/`

## Postman Collection
Import the JSON file included in this repo to test APIs easily.

## ⚙️ How to run locally

```bash
# Clone the repo
git clone https://github.com/SatvickShekhawat31/Test-Project.git
cd Test-Project

# Create & activate virtual env
python -m venv env
# Windows
env\Scripts\activate
# Mac/Linux
source env/bin/activate

# Install requirements
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
```
---

## 🧪 API Testing (Postman)
- Import postman_collection.json into Postman
- Contains ready-to-use requests: Register, Login, Upload, List, Download etc.
- Test permissions (only ops can upload, only clients can download)

---

## ✏ Test Cases

- File: api/tests.py
- Covers register, login, upload, download, permission checks
- Run all:
```bash
python manage.py test
```

---

## ✔️ Deployment Plan

- Cloud server (e.g., AWS EC2, DigitalOcean, Render, etc.)
- Gunicorn + Nginx for serving Django app securely
- Use environment variables for sensitive info (SECRET_KEY, DB credentials, etc.)
- Use HTTPS (Let's Encrypt SSL)
- Database: SQLite (dev) → upgrade to PostgreSQL (prod)
- Static files: AWS S3 / DigitalOcean Spaces ya locally via collectstatic 
- Optional: Use Docker to containerize the app

--- 

## 🔒 Security

- Encrypted download URLs
- Only client users can access download links
- Ops users can upload but cannot download

---

## 📂 Project Structure

```bash
testproject/
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── testproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── postman_collection.json
├── requirements.txt
└── manage.py
```

# Test-Project

## 📦 Test Project – Secure File Sharing System

A Django REST API for secure file sharing between **Ops Users** and **Client Users**.  
Supports registration, login, file upload (only by Ops users), secure download link generation, and profile management.

---

### 🚀 Features
- Register & login for Ops and Client users
- Ops users can upload only `.pptx`, `.docx`, `.xlsx` files
- Clients get encrypted download links for files
- Token-based authentication
- Ready Postman collection for testing

---

### ⚙️ How to run locally

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

## API Endpoints (examples)
- `POST /api/register/`
- `POST /api/login/`
- `GET /api/profile/`
- `POST /api/files/`
- `GET /api/files/`
- `GET /download/<file_id>/`

## Postman Collection
Import the JSON file included in this repo to test APIs easily.

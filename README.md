# COMP693-Shopping-Centre-Dashboard
# 🏙️ Shopping Centre Dashboard

A web application built with **Flask + MySQL + Bootstrap + Leaflet** to manage and explore shopping centres in New Zealand.  
It supports city summaries, shopping centre details, staff management, and role-based access control (Visitor, Editor, Admin).

---

## ✨ Features

### Visitor (no login required)
- View city summaries and number of centres.
- Browse shopping centres by city.
- Search centres and preview them on a map.
- View details with classification, type, size, and parking info.

### Staff (login required)
- **Editor**:
  - Create new shopping centres.
  - Edit cities and centres.
- **Admin**:
  - All Editor permissions.
  - Delete cities and centres.
  - Manage staff users (create, edit, deactivate, reset passwords).

### Core Functionality
- 📍 Interactive **map** of shopping centres with numbered markers (Leaflet + OpenStreetMap).
- 🔍 **Search** with datalist and quick filtering.
- 🗂️ **CRUD operations** for cities and centres.
- 👥 **Role-based access control** (Visitor / Editor / Admin).
- 📸 Image upload for cities and centres.
- 🛠️ Staff profile management (update details, change password).
- 🗄️ MySQL backend with normalized schema.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10, Flask
- **Database**: MySQL 8.x
- **Frontend**: Bootstrap 5 (Bootswatch Zephyr theme), Font Awesome
- **Map**: Leaflet.js + OpenStreetMap + Nominatim Geocoding
- **Auth**: Werkzeug password hashing, session management
- **Deployment**: PythonAnywhere / local development with VS Code
- **Version Control**: GitHub

---

## 📂 Project Structure
- app/
- ├── init.py
- ├── templates/
- │ ├── layout.html
- │ ├── citysummary.html
- │ ├── centrelist.html
- │ ├── centredetails.html
- │ ├── centrenew.html
- │ ├── login.html
- │ ├── profile.html
- │ ├── manage_staff.html
- │ └── ...
- ├── static/
- │ ├── css/
- │ ├── js/
- │ └── images/
- ├── src/
- │ ├── route/
- │ │ ├── citysummary.py
- │ │ ├── centrelist.py
- │ │ ├── centrecreate.py
- │ │ ├── auth.py
- │ │ └── staff_admin.py
- │ ├── model/
- │ │ ├── geo.py
- │ │ └── image.py
- └── db.py

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/shopping-centre-dashboard.git
cd shopping-centre-dashboard
```
### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Database Setup
- Create a MySQL database.
- Run schema scripts (create_databases.sql).
- Insert sample data for cities, classifications, centre types and staff users.(populate_database.sql)
### 5. Configure Environment
### 6. Run Development Server
```bash
python run.py
```
Visit http://127.0.0.1:5000

---

## 🔑 Roles & Permissions
| Role    | Create | Edit | Delete | Staff Management |
| ------- | ------ | ---- | ------ | ---------------- |
| Visitor | ❌      | ❌    | ❌      | ❌                |
| Editor  | ✅      | ✅    | ❌      | ❌                |
| Admin   | ✅      | ✅    | ✅      | ✅                |

---

## 🚀 Deployment
### PythonAnywhere
- Push code to GitHub.
- Pull to PythonAnywhere.
- Install dependencies in virtualenv.
- Configure WSGI app to point to app.
- Run database migrations.

---

## 👩‍💻 Author
Developed by Tina Ma 1061935 (Lincoln University, COMP693 Industry Project).

---

## 📜 License
This project is for educational purposes (COMP693 Industry Project).
You may fork and adapt it, but please credit the original author.



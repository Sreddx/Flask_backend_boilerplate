# Flask Project Template

## 🚀 Introduction

This repository serves as a **template for Flask-based web applications**, designed following industry **best practices**. It includes essential tools and libraries for **development, testing, and deployment**. 

This template is **frontend-friendly** and allows developers to spin up the backend **quickly** using Docker or local environments.

## 🛠 Minimum Requirements

To use this template, ensure you have the following installed:

- **Python 3.9 or higher**
- **pip** (Python package manager)
- **PostgreSQL** (for production, SQLite is used as a fallback in development)
- **Docker** (optional, for containerized environments)
- **Virtual environment** (recommended but not mandatory)

## 📌 Best Practices and Nomenclatures

### **1️⃣ Code Organization**
- Modular **Blueprints** for route management.
- `models/` for **SQLAlchemy ORM models**.
- `services/` for **business logic** and database interactions.
- `blueprints/` to **separate API routes** for authentication, users, etc.

### **2️⃣ Database Management**
- **SQLAlchemy** for ORM-based queries.
- **Flask-Migrate** for database migrations.
- **Uses SQLite by default in development/testing** (switch to PostgreSQL for full dev/production or cloud environment).

### **3️⃣ Environment Management**
- **Dynamic `.env` support** for configuration.
- Different environments: **Development, QA, Production**.
- **Validation for missing environment variables** (production/QA requires `DATABASE_URL`).

### **4️⃣ Logging & Debugging**
- **Dynamic log levels** (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- Logging format includes **timestamps, log level, and module name**.
- Logs are written to **console (stdout)** for easy debugging.

## 🔧 How to Run the Project Locally

### **1️⃣ Set Up a Virtual Environment**

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Configure Environment Variables**

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Modify `.env` with your settings.

### **4️⃣ Initialize the Database**

**If using SQLite (Development):**

```bash
flask db upgrade
```

**If using PostgreSQL (Production):** Ensure `DATABASE_URL` is set, then run:

```bash
flask db upgrade
```

### **5️⃣ Run the Application**

```bash
flask run
```

The backend will be available at [http://localhost:5000](http://localhost:5000).

## 🐳 Running with Docker

### **1️⃣ Using `run_docker.sh` for Quick Setup**
For frontend developers or quick deployments, the `run_docker.sh` script automates everything.

#### ✅ Automatic Features
- Detects `.env` and loads environment variables.
- Cleans up old Docker containers and images.
- Runs Flask in development mode or Gunicorn in production mode.
- Supports different environments dynamically.

#### 🚀 Running in Development Mode
```bash
bash run_docker.sh development
```
- Uses Flask's built-in development server (`flask run`).
- Runs on port 5000 (or port specified in `.env`).
- Uses SQLite if no `DATABASE_URL` is provided.

#### 🚀 Running in Production Mode
```bash
bash run_docker.sh production
```
- Runs Gunicorn WSGI server.
- Runs on port 8000 (or the port set in `.env`).
- Requires `DATABASE_URL` (fails if missing).

#### ⚡ Running Without Arguments
If no argument is provided, the script defaults to development:

```bash
bash run_docker.sh
```

### **2️⃣ Manually Building & Running the Docker Container**
If you prefer not to use `run_docker.sh`, you can manually build and run:

#### Build the Docker Image
**Development:**

```bash
docker build -t my-flask-app -f Dockerfile.dev .
```

**Production:**

```bash
docker build -t my-flask-app -f Dockerfile.prod .
```

#### Run the Container

```bash
docker run --env-file .env -p 5000:5000 --name my-flask-app-container my-flask-app
```

## 🔄 Dockerfile Overview

### **Development (`Dockerfile.dev`)**
- Uses Flask’s built-in development server.
- Supports hot-reloading.
- Uses SQLite as fallback.

### **Production (`Dockerfile.prod`)**
- Uses Gunicorn (high-performance WSGI server).
- Requires PostgreSQL or another database.
- Fails if `DATABASE_URL` is missing.

## 📄 Sample `.env` File

```ini
# General Configuration
FLASK_APP=app.py
FLASK_ENV=development  # Change to "production" for production mode
FLASK_DEBUG=1  # Set to 0 in production

# Server Configuration
FLASK_RUN_HOST=0.0.0.0  # Flask should listen on all interfaces inside the container
FLASK_RUN_PORT=5000  # Port for Flask dev server
GUNICORN_PORT=8000  # Port for Gunicorn in production

# Database Configuration
DATABASE_URL=postgresql://username:password@dbserver/dbname  # Required for production
DEV_DATABASE_URL=sqlite:///development.db  # SQLite fallback for development
TEST_DATABASE_URL=sqlite:///testing.db  # SQLite for testing

# Security Keys
SECRET_KEY=super-secret-key
JWT_SECRET_KEY=super-secret-jwt-key

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500  # Allowed origins for frontend apps

# Logging Configuration
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Other Third-party API Keys
THIRD_PARTY_API_KEY=someapikey123
```

## 🚀 Future Updates
In upcoming releases, we will add:

- ✅ Unit Testing Setup
- ✅ Customizable GitHub Actions for Pull Requests & CI/CD Deployments.
- ✅ Swagger/OpenAPI Documentation.

## 🎯 Final Notes
- ✅ Frontend developers can start the backend in seconds with `run_docker.sh`.
- ✅ Enforces required env variables in production/QA (ensuring stability).
- ✅ Supports both manual & automated Docker builds.
- ✅ Follows best practices for security & maintainability.

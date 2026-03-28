# BizBoard — Business Dashboard

A simple business product dashboard built with Python (Flask) + SQLite.

## Files

```
bizboard/
├── app.py              ← Main Python app (Flask)
├── requirements.txt    ← Python dependencies
├── bizboard.db         ← SQLite database (auto-created on first run)
└── templates/
    ├── auth.html       ← Login & Signup page
    └── dashboard.html  ← Main dashboard
```

## Setup & Run

### 1. Install Python
Make sure Python 3 is installed: https://python.org

### 2. Install Flask
Open terminal in the `bizboard` folder and run:
```
pip install flask
```

### 3. Run the app
```
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

That's it. The SQLite database file (`bizboard.db`) is created automatically on first run.

## Database Structure

**users table**
| Column   | Type    | Description              |
|----------|---------|--------------------------|
| id       | INTEGER | Primary key              |
| org      | TEXT    | Organisation name        |
| field    | TEXT    | Business field           |
| email    | TEXT    | Unique email (login)     |
| password | TEXT    | SHA-256 hashed password  |

**products table**
| Column     | Type    | Description              |
|------------|---------|--------------------------|
| id         | INTEGER | Primary key              |
| user_id    | INTEGER | Foreign key → users.id   |
| name       | TEXT    | Product name             |
| quantity   | INTEGER | Stock quantity           |
| price      | REAL    | Unit price               |
| detail     | TEXT    | Optional description     |
| created_at | TEXT    | Date added               |

## Deploy Online (optional)
To make it accessible from any device, deploy to:
- **Railway** → https://railway.app (free tier available)
- **Render**  → https://render.com (free tier available)
- **PythonAnywhere** → https://pythonanywhere.com (free tier available)

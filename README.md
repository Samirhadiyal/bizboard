# BizBoard - Multi Tenant Business Dashboard

## 📌 Overview
BizBoard is a web-based application built using **Flask (Python)** that demonstrates the concept of a **Multi Tenant SaaS (Software as a Service)** system.

The application allows multiple business users to register, manage their products, and access a dashboard. Each user belongs to an organization (`org`), which acts as the **tenant identifier**, enabling logical separation of data within a shared system.

---

### Key Idea:
- A single application serves multiple users
- All data is stored in the same database
- Each user is associated with an organization (`org`)
- Data access is restricted based on user identity

> This demonstrates **logical data isolation**, a core concept of multi-tenancy.

---

## ⚙️ Tech Stack

### Backend
- Python
- Flask

### Database
- SQLite3 (lightweight relational database)

### Frontend
- HTML
- CSS
- Flask Templates (Jinja2)

### Authentication & Security
Client (Browser)
<br>
↓
<br>
Flask Application (app.py)
<br>
↓
<br>
SQLite Database (bizboard.db)

---

## 🗄️ Database Schema

### Users Table
- `id` (Primary Key)
- `org` (Organization / Tenant identifier)
- `field` (Business category)
- `email` (Unique)
- `password` (Hashed)

### Products Table
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `name`
- `quantity`
- `price`
- `detail`
- `created_at`

---

## 🔄 Application Workflow

1. User registers with organization details
2. User logs into the system
3. Session stores user identity
4. User adds and manages products
5. System retrieves only user-specific data
6. Dashboard displays product information

---

## 📊 Features

- User Registration and Login
- Secure Authentication System
- Product Management (Add and View)
- Dashboard Interface
- Session Handling
- Password Hashing

---

## ☁️ Cloud Computing Relevance

This project demonstrates key cloud concepts:
- Software as a Service (SaaS)
- Multi-tenant architecture
- Shared resource utilization
- Centralized application model

---

## 🚀 How to Run the Project

### 1. Clone Repository
- Password hashing using SHA-256
- Session-based authentication (Flask sessions)


`git clone https://github.com/Samirhadiyal/bizboard.git`

---

### 2. Install Dependencies
- `pip install Flask`

### 3. Run Application
- `python app.py`

### 4. Access in Browser
- https://

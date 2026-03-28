# BizBoard - Multi Tenant Business Dashboard

## 📌 Overview
BizBoard is a web-based application built using **Flask (Python)** that demonstrates the concept of a **Multi Tenant SaaS (Software as a Service)** system.

The application allows multiple business users to register, manage their products, and access a dashboard. Each user belongs to an organization (`org`), which acts as the **tenant identifier**, enabling logical separation of data within a shared system.

---

## 🎯 Objective
The main objectives of this project are:
- To understand and implement **Multi Tenant SaaS architecture**
- To allow multiple organizations to use a single application
- To ensure **logical data isolation** between users
- To build a simple business product management dashboard

---

## 🧠 Multi-Tenant Architecture

This project follows a **shared database, shared schema** approach.

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
- Password hashing using SHA-256
- Session-based authentication (Flask sessions)

---

## 🏗️ System Architecture

# Café Management System

A comprehensive café management system built with Flask, featuring menu management, order processing, user authentication, and administrative controls.

![Café Management System](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents

- [✨ Features](#-features)

- [🛠 Tech Stack](#-tech-stack)

- [📦 Installation](#-installation)

- [⚙️ Configuration](#️-configuration)

- [Running the Application](#running-the-application)

- [API Documentation](#api-documentation)

- [Project Maintenance](#project-maintenance)

- [Testing](#testing)

- [Deployment](#deployment)

- [License](#license)

## ✨ Features

### For Customers

- Browse menu with categories and dietary filters
- User authentication and profile management
- Order placement and tracking
- Order history
- Responsive design for all devices

### For Staff

- Dashboard with order notifications
- Order management
- Table management
- Basic reporting

### For Administrators

- Full menu management
- User management
- Advanced reporting and analytics
- System configuration
- Database administration

## 🛠 Tech Stack

### Backend

- **Python 3.9+**
- **Flask 2.0+** - Web framework
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Flask-Login** - User session management
- **Flask-WTF** - Form handling
- **Flask-Mail** - Email notifications

### Frontend

- **HTML5/CSS3**
- **Bootstrap 5** - Responsive design
- **JavaScript** - Client-side interactivity
- **jQuery** - DOM manipulation
- **Font Awesome** - Icons

### Database

- **SQLite** (Development)
- **PostgreSQL** (Production)

### Development Tools

- **Git** - Version control
- **Pip** - Package management
- **Pytest** - Testing framework
- **Black** - Code formatting
- **Flake8** - Linting

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/cafe-management-system.git
   cd cafe-management-system
   ```

2. **Create and activate a virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Copy the example environment file and update it with your settings:

   ```bash
   cp .env.example .env
   ```

    ```bash
    pip install Flask
    ```

### Running the Application

1. Run the Flask app:

    ```bash
    python app.py
    ```

2. Open your browser and navigate to:

    ```text
    http://127.0.0.1:5000/
    ```

### Notes

- The SQLite database will be automatically created and seeded with sample menu items on first run.
- Admin panel is accessible at `/admin` to view orders.

## Project Maintenance

- To add or modify menu items, update the `seed_menu()` function in `app.py` or extend with an admin interface.
- Orders are stored in the `orders` table in the SQLite database (`database.db` file).

## License

This project is for demonstration purposes.

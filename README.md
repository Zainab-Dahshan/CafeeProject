# ☕ Café Management System

A modern, responsive café management system built with Flask, designed to streamline café operations from order taking to inventory management. The system features a clean, intuitive interface for both customers and staff, with robust backend functionality.

![Café Management System](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-7952b3)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub last commit](https://img.shields.io/github/last-commit/Zainab-Dahshan/CafeeProject)](https://github.com/Zainab-Dahshan/CafeeProject/commits/master)

## 📋 Table of Contents

- [✨ Features](#-features)

- [🛠 Tech Stack](#-tech-stack)

- [📦 Installation](#-installation)

- [⚙️ Configuration](#️-configuration)

- [Running the Application](#running-the-application)

- [API Documentation] (#api-documentation)

- [Project Maintenance](#project-maintenance)

- [Testing] (#testing)

- [Deployment] (#deployment)

- [License](#license)

## ✨ Features

### For Customers

- 🍽️ Browse an interactive menu with categories and dietary filters
- 🔐 Secure user authentication and profile management
- 🛒 Easy order placement with real-time updates
- 📱 Responsive design that works on all devices
- 📋 View order history and receipts
- 📍 Delivery and pickup options

### For Staff

- 📊 Interactive dashboard with live order notifications
- 📝 Manage and update order status in real-time
- 🏷️ Table management system
- 📈 Basic sales and performance reporting
- 🔄 Quick order modifications and updates

### For Administrators

- 👥 User and role management
- 📦 Menu and inventory management
- 💰 Financial reporting and analytics
- ⚙️ System configuration and settings
- 📊 Comprehensive business insights

- Full menu management
- User management
- Advanced reporting and analytics
- System configuration
- Database administration

## 🛠 Tech Stack

### Frontend

- **HTML5, CSS3, JavaScript** - Core web technologies
- **Bootstrap 5** - Responsive design framework
- **Font Awesome** - Icons and visual elements
- **jQuery** - DOM manipulation and AJAX requests

### Backend

- **Python 3.9+** - Core programming language
- **Flask 2.0+** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **Flask-WTF** - Form handling and validation

### Database

- **SQLite** - Development database
- **Flask-Migrate** - Database migrations

### Development Tools

- **Git** - Version control
- **Pip** - Package management
- **Virtual Environment** - Dependency isolation
- **Flask-DebugToolbar** - Development debugging

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git (for version control)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Zainab-Dahshan/CafeeProject.git
   cd CafeeProject
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the configuration as needed

5. **Initialize the database**

   ```bash
   flask db upgrade
   ```

### Starting the Development Server

1. **Start the development server**

   ```bash
   flask run
   ```

2. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Admin interface available at `http://localhost:5000/admin`

## 📝 Usage

### Customer Interface

- Browse the menu and add items to your cart
- Create an account or log in to place orders
- Choose between delivery and pickup options
- Track your order status in real-time

### Admin Interface

- Access the admin dashboard at `/admin`
- Manage menu items, categories, and inventory
- View and process orders
- Generate reports and view analytics

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Bootstrap](https://getbootstrap.com/) - For the responsive design
- [Font Awesome](https://fontawesome.com/) - For the beautiful icons
- All contributors who have helped shape this project

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

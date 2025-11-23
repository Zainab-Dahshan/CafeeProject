# Maryam's Café Website

A simple website for a small café built with Python Flask, SQLite, HTML, CSS, and JavaScript.

## Features

- Home page displaying the café menu
- Order page for customers to select items and submit orders
- Admin panel to view new orders
- Responsive and clean design

## Project Structure

```text
cafeeproject/
├── app.py
├── database.db
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── order.html
│   └── admin.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.x installed on your machine
- pip (Python package installer)

### Installation

1. Clone or download the project files.

2. Create and activate a virtual environment (recommended):

    ```bash
    python -m venv venv

    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

3. Install required Python packages:

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

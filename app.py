try:
    from flask import Flask, render_template, request, redirect, url_for
except Exception as e:
    import sys
    sys.stderr.write(
        "Missing dependency: Flask is not installed in the current Python environment.\n"
        "Install it with: pip install Flask\n"
        "Or via requirements file: pip install -r requirements.txt\n"
        f"Original error: {e}\n"
    )
    sys.exit(1)

import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create menu_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
    ''')
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def seed_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if menu is empty
    cursor.execute('SELECT COUNT(*) FROM menu_items')
    count = cursor.fetchone()[0]
    if count == 0:
        # Insert some sample menu items
        sample_items = [
            ('Cappuccino', 'Espresso with steamed milk and foam', 3.5),
            ('Latte', 'Espresso with steamed milk', 3.0),
            ('Espresso', 'Strong black coffee', 2.0),
            ('Tea', 'Assorted herbal teas', 2.5),
            ('Croissant', 'Buttery flaky pastry', 2.75),
            ('Muffin', 'Blueberry muffin', 2.5)
        ]
        cursor.executemany('INSERT INTO menu_items (name, description, price) VALUES (?, ?, ?)', sample_items)
        conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = get_db_connection()
    menu_items = conn.execute('SELECT * FROM menu_items').fetchall()
    conn.close()
    return render_template('home.html', menu_items=menu_items)

@app.route('/order', methods=['GET', 'POST'])
def order():
    conn = get_db_connection()
    menu_items = conn.execute('SELECT * FROM menu_items').fetchall()
    if request.method == 'POST':
        selected_ids = request.form.getlist('items')
        if not selected_ids:
            # No items selected, reload order page with a message could be added (not implemented here)
            return redirect(url_for('order'))
        selected_items = []
        for item_id in selected_ids:
            item = conn.execute('SELECT * FROM menu_items WHERE id = ?', (item_id,)).fetchone()
            if item:
                selected_items.append({'id': item['id'], 'name': item['name'], 'price': item['price']})
        # Save order items as JSON string
        items_json = json.dumps(selected_items)
        conn.execute('INSERT INTO orders (items) VALUES (?)', (items_json,))
        conn.commit()
        conn.close()
        return render_template('order.html', menu_items=menu_items, success=True)
    conn.close()
    return render_template('order.html', menu_items=menu_items)

@app.route('/admin')
def admin():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders ORDER BY timestamp DESC').fetchall()
    conn.close()
    # Parse JSON items for display
    orders_parsed = []
    for order in orders:
        items = json.loads(order['items'])
        orders_parsed.append({
            'id': order['id'],
            'items': items,
            'timestamp': order['timestamp']
        })
    return render_template('admin.html', orders=orders_parsed)

if __name__ == '__main__':
    init_db()
    seed_menu()
    app.run(debug=True)

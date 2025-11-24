from flask import render_template, redirect, url_for, flash, request, current_app, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime
from .. import db
from ..models import MenuItem, Order, OrderItem
from . import main
from .forms import MenuItemForm, OrderForm, SearchForm
from ..utils.decorators import admin_required

@main.route('/')
def index():
    """Render the home page with featured menu items."""
    # Get featured menu items (you can adjust the query as needed)
    featured_items = MenuItem.query.filter_by(is_featured=True, is_available=True).all()
    
    # Get menu categories for navigation
    categories = MenuItem.get_categories()
    
    return render_template('main/index.html', 
                         featured_items=featured_items,
                         categories=categories)

@main.route('/menu')
def menu():
    """Display the full menu with all available items."""
    # Get all available menu items grouped by category
    menu_items = {}
    categories = MenuItem.get_categories()
    
    for category in categories:
        items = MenuItem.query.filter_by(
            category=category, 
            is_available=True
        ).order_by(MenuItem.name).all()
        if items:  # Only add categories that have items
            menu_items[category] = items
    
    return render_template('main/menu.html', 
                         menu_items=menu_items,
                         categories=categories)

@main.route('/menu/<int:id>')
def menu_item(id):
    """Display details for a specific menu item."""
    item = MenuItem.query.get_or_404(id)
    if not item.is_available and not current_user.is_admin:
        abort(404)
    
    # Get recommended items (e.g., other items from the same category)
    recommended = MenuItem.query.filter(
        MenuItem.id != item.id,
        MenuItem.category == item.category,
        MenuItem.is_available == True
    ).limit(4).all()
    
    return render_template('main/menu_item.html', 
                         item=item,
                         recommended=recommended)

@main.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    """Handle new orders."""
    form = OrderForm()
    
    # Get available menu items for the select field
    menu_items = [(str(item.id), item.name) 
                 for item in MenuItem.query.filter_by(is_available=True).all()]
    form.menu_items.choices = menu_items
    
    if form.validate_on_submit():
        # Create new order
        order = Order(
            user_id=current_user.id,
            order_type=form.order_type.data,
            table_number=form.table_number.data if form.order_type.data == 'dine_in' else None,
            customer_name=current_user.get_full_name() or current_user.username,
            customer_email=current_user.email,
            customer_phone=current_user.phone,
            status='pending'
        )
        
        # Add order items
        for item_id, quantity in form.menu_items.data.items():
            if int(quantity) > 0:
                menu_item = MenuItem.query.get(item_id)
                if menu_item and menu_item.is_available:
                    order_item = OrderItem(
                        menu_item_id=menu_item.id,
                        item_name=menu_item.name,
                        item_price=menu_item.price,
                        quantity=quantity
                    )
                    order.items.append(order_item)
        
        # Calculate totals
        order.calculate_totals()
        
        # Save to database
        db.session.add(order)
        db.session.commit()
        
        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('main.order_confirmation', order_id=order.id))
    
    return render_template('main/order.html', form=form)

@main.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    """Display order confirmation page."""
    order = Order.query.get_or_404(order_id)
    
    # Ensure the current user owns the order or is an admin
    if order.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('main/order_confirmation.html', order=order)

@main.route('/my-orders')
@login_required
def my_orders():
    """Display the current user's order history."""
    page = request.args.get('page', 1, type=int)
    pagination = Order.query.filter_by(user_id=current_user.id)\
                           .order_by(Order.order_date.desc())\
                           .paginate(page=page, per_page=10, error_out=False)
    
    orders = pagination.items
    return render_template('main/my_orders.html', 
                         orders=orders,
                         pagination=pagination)

@main.route('/about')
def about():
    """Display the about page."""
    return render_template('main/about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact form submissions."""
    form = ContactForm()
    
    if form.validate_on_submit():
        # In a real application, you would send an email here
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('main/contact.html', form=form)

@main.route('/search')
def search():
    """Search for menu items."""
    form = SearchForm()
    query = request.args.get('q', '')
    
    if query:
        # Search in name and description
        results = MenuItem.query.filter(
            (MenuItem.name.ilike(f'%{query}%')) |
            (MenuItem.description.ilike(f'%{query}%')),
            MenuItem.is_available == True
        ).all()
    else:
        results = []
    
    return render_template('main/search.html', 
                         query=query,
                         results=results,
                         form=form)

# API Endpoints
@main.route('/api/menu/items')
def get_menu_items():
    """API endpoint to get all available menu items."""
    items = MenuItem.query.filter_by(is_available=True).all()
    return jsonify([item.to_dict() for item in items])

@main.route('/api/menu/categories')
def get_menu_categories():
    """API endpoint to get all menu categories."""
    categories = MenuItem.get_categories()
    return jsonify(categories)

@main.route('/api/orders', methods=['POST'])
@login_required
def create_order():
    """API endpoint to create a new order."""
    data = request.get_json()
    
    if not data or 'items' not in data:
        return jsonify({'error': 'No items provided'}), 400
    
    try:
        order = Order(
            user_id=current_user.id,
            order_type=data.get('order_type', 'dine_in'),
            table_number=data.get('table_number'),
            customer_name=current_user.get_full_name() or current_user.username,
            customer_email=current_user.email,
            customer_phone=current_user.phone,
            status='pending'
        )
        
        # Add order items
        for item_data in data['items']:
            menu_item = MenuItem.query.get(item_data.get('id'))
            if menu_item and menu_item.is_available:
                order_item = OrderItem(
                    menu_item_id=menu_item.id,
                    item_name=menu_item.name,
                    item_price=menu_item.price,
                    quantity=item_data.get('quantity', 1)
                )
                order.items.append(order_item)
        
        # Calculate totals
        order.calculate_totals()
        
        # Save to database
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order.id,
            'order_number': order.order_number
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error creating order: {str(e)}')
        return jsonify({'error': 'Failed to create order'}), 500

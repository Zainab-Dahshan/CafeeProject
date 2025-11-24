from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, Optional, NumberRange, ValidationError
from flask_wtf.file import FileField, FileAllowed
from ..models import MenuItem

class MenuItemForm(FlaskForm):
    """Form for adding/editing menu items."""
    name = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    category = StringField('Category', validators=[DataRequired(), Length(max=50)])
    is_available = BooleanField('Available', default=True)
    is_featured = BooleanField('Featured', default=False)
    calories = IntegerField('Calories', validators=[Optional(), NumberRange(min=0)])
    is_vegetarian = BooleanField('Vegetarian', default=False)
    is_vegan = BooleanField('Vegan', default=False)
    is_gluten_free = BooleanField('Gluten Free', default=False)
    image = FileField('Item Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Item')
    
    def validate_name(self, field):
        """Check if menu item name is already in use."""
        # Skip if we're editing the same item
        if hasattr(self, 'item_id'):
            existing = MenuItem.query.filter(
                MenuItem.name == field.data,
                MenuItem.id != self.item_id
            ).first()
        else:
            existing = MenuItem.query.filter_by(name=field.data).first()
            
        if existing:
            raise ValidationError('A menu item with this name already exists.')


class OrderItemForm(FlaskForm):
    """Form for a single order item (used in the order form)."""
    menu_item_id = IntegerField('Menu Item', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(), 
        NumberRange(min=1, max=20, message='Quantity must be between 1 and 20')
    ], default=1)
    special_instructions = TextAreaField('Special Instructions', validators=[Optional()])


class OrderForm(FlaskForm):
    """Form for placing a new order."""
    order_type = SelectField('Order Type', 
                           choices=[
                               ('dine_in', 'Dine In'),
                               ('takeout', 'Takeout'),
                               ('delivery', 'Delivery')
                           ], 
                           validators=[DataRequired()])
    table_number = IntegerField('Table Number', validators=[
        Optional(),
        NumberRange(min=1, max=100, message='Table number must be between 1 and 100')
    ])
    menu_items = FieldList(FormField(OrderItemForm), min_entries=1)
    submit = SubmitField('Place Order')
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Initialize at least one order item
        if not self.menu_items:
            self.menu_items.append_entry()
    
    def validate_table_number(self, field):
        """Validate table number is provided for dine-in orders."""
        if self.order_type.data == 'dine_in' and not field.data:
            raise ValidationError('Table number is required for dine-in orders.')


class ContactForm(FlaskForm):
    """Form for the contact page."""
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Send Message')


class SearchForm(FlaskForm):
    """Form for searching menu items."""
    query = StringField('Search', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', coerce=str, validators=[Optional()])
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        # Dynamically populate categories
        self.category.choices = [('', 'All Categories')] + [
            (category, category) for category in MenuItem.get_categories()
        ]


class ReservationForm(FlaskForm):
    """Form for making a reservation."""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    date = StringField('Date', validators=[DataRequired()])  # Will be handled by datepicker
    time = StringField('Time', validators=[DataRequired()])  # Will be handled by timepicker
    guests = IntegerField('Number of Guests', validators=[
        DataRequired(), 
        NumberRange(min=1, max=20, message='Number of guests must be between 1 and 20')
    ], default=2)
    special_requests = TextAreaField('Special Requests', validators=[Optional()])
    submit = SubmitField('Make Reservation')
    
    def validate_date(self, field):
        """Validate the reservation date."""
        from datetime import datetime
        try:
            date_obj = datetime.strptime(field.data, '%Y-%m-%d').date()
            if date_obj < datetime.utcnow().date():
                raise ValidationError('Reservation date cannot be in the past.')
        except ValueError:
            raise ValidationError('Invalid date format. Please use YYYY-MM-DD.')
    
    def validate_time(self, field):
        """Validate the reservation time."""
        try:
            time_obj = datetime.strptime(field.data, '%H:%M').time()
            # Example: Only allow reservations between 8 AM and 10 PM
            if time_obj < datetime.strptime('08:00', '%H:%M').time() or \
               time_obj > datetime.strptime('22:00', '%H:%M').time():
                raise ValidationError('Reservations are only available between 8 AM and 10 PM.')
        except ValueError:
            raise ValidationError('Invalid time format. Please use HH:MM (24-hour format).')

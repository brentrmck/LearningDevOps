from flask import Flask, render_template, request, redirect, url_for, session
import os
from forms import MerchForm  # Import the MerchForm
from models import Cart, CartItem, MerchItem, db  # Import Cart, CartItem, MerchItem, and db
import logging
from logging.handlers import RotatingFileHandler


# Initialize Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_key')

# Initialize db with the app
db.init_app(app)

# Define the full path to the logs directory
log_dir = '/Users/brentmckinney/PycharmProjects/learning_devops/logs'

# Ensure the logs directory exists
os.makedirs(log_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# File paths for the logs
app_log_path = os.path.join(log_dir, 'app.log')
access_log_path = os.path.join(log_dir, 'access.log')

# Set up application logging
if not app.debug:
    app_log_handler = RotatingFileHandler(app_log_path, maxBytes=10000, backupCount=1)
    app_log_handler.setLevel(logging.INFO)
    app_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(app_log_handler)

# Set up access logging (for HTTP requests)
access_log_handler = RotatingFileHandler(access_log_path, maxBytes=10000, backupCount=1)
access_log_handler.setLevel(logging.INFO)
access_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Log HTTP requests
@app.before_request
def log_request():
    app.logger.info(f"Request: {request.method} {request.url}")
    # Also log in the access log
    access_log_handler.emit(logging.LogRecord(
        name='access',
        level=logging.INFO,
        pathname=request.path,
        lineno=0,
        msg=f"Request: {request.method} {request.url}",
        args=None,
        exc_info=None
    ))



# Define routes
@app.route("/")
def index():
    app.logger.info("Home page visited")
    return render_template("index.html")

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    cart_id = session.get('cart', None)

    if not cart_id:
        new_cart = Cart()
        db.session.add(new_cart)
        db.session.commit()
        session['cart'] = new_cart.id
        cart_id = new_cart.id

    item = MerchItem.query.get(item_id)

    if item:
        cart_item = CartItem.query.filter_by(cart_id=cart_id, merch_item_id=item.id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            new_cart_item = CartItem(quantity=1, merch_item_id=item.id, cart_id=cart_id)
            db.session.add(new_cart_item)
        db.session.commit()
        return redirect(url_for('merch'))

    return "Item not found", 404

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = MerchForm()  # Initialize the form
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        quantity = form.quantity.data
        price = form.price.data
        description = form.description.data
        new_item = MerchItem(name=name, quantity=quantity, price=price, description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('merch'))
    return render_template('add_item.html', form=form)

@app.route('/cart')
def cart():
    cart_id = session.get('cart', None)
    if not cart_id:
        return redirect(url_for('merch'))

    cart = Cart.query.get(cart_id)
    if not cart:
        return redirect(url_for('merch'))

    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    total_price = sum(item.quantity * item.merch_item.price for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route("/merch")
def merch():
    app.logger.info("Merch page visited")
    items = MerchItem.query.all()
    return render_template("merch.html", items=items)

@app.route("/music")
def music():
    return render_template("music.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/tour")
def tour():
    return render_template("tour.html")

if __name__ == "__main__":
    # Initialize the database within the app context
    with app.app_context():
        db.create_all()  # This will create all tables including Cart and CartItem

    app.run(host="0.0.0.0", port=5000, debug=True)

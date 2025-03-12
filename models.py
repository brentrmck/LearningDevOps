from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy, but don't initialize it yet
db = SQLAlchemy()

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    merch_item_id = db.Column(db.Integer, db.ForeignKey('merch_item.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

class MerchItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    cart_items = db.relationship('CartItem', backref='merch_item', lazy=True)

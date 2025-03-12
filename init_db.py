from app import app, db, MerchItem, Cart, CartItem  # Import models
with app.app_context():
    db.drop_all()  # Be cautious with this line; it drops all tables
    db.create_all()

    # Insert sample data if the table is empty
    if not MerchItem.query.first():
        sample_items = [
            MerchItem(name='Band Tee', quantity=1, price=20.0, description='100% cotton, sizes S-XL'),
            MerchItem(name='Vinyl Record', quantity=1, price=30.0, description='Limited edition 12" vinyl')
        ]
        db.session.add_all(sample_items)
        db.session.commit()

    if not Cart.query.first():
        new_cart = Cart()
        db.session.add(new_cart)
        db.session.commit()

    # Print all items, carts, and cart_items to verify
    print("MerchItems:", MerchItem.query.all())
    print("Carts:", Cart.query.all())
    print("CartItems:", CartItem.query.all())

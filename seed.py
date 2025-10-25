from __init__ import create_app, db
from models import Product

app = create_app()

with app.app_context():
    # Delete all existing products
    Product.query.delete()

    # Create new products
    product1 = Product(
        name='Sample Product 1',
        description='This is a description for Sample Product 1.',
        price=19.99,
        stock=10,
        image_url='https://via.placeholder.com/300'
    )
    product2 = Product(
        name='Sample Product 2',
        description='This is a description for Sample Product 2.',
        price=29.99,
        stock=5,
        image_url='https://via.placeholder.com/300'
    )

    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()

    print('Database seeded!')

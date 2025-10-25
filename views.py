from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import db
from .models import Product, CartItem, Order, OrderItem
from .forms import AddToCartForm

views = Blueprint('views', __name__)

@views.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@views.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddToCartForm()
    return render_template('product.html', product=product, form=form)

@views.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    form = AddToCartForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=quantity)
            db.session.add(cart_item)
        db.session.commit()
        flash('Item added to your cart!', 'success')
    else:
        flash('Invalid quantity.', 'danger')
    return redirect(url_for('views.cart'))

@views.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


# Checkout Route
@views.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if not cart_items:
        flash('Your cart is empty.', 'danger')
        return redirect(url_for('views.cart'))
    new_order = Order(user_id=current_user.id, total_price=total_price)
    db.session.add(new_order)
    for item in cart_items:
        new_order_item = OrderItem(
            order=new_order,
            product_id=item.product.id,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )
        db.session.add(new_order_item)
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('views.orders'))


# Order History Route
@views.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

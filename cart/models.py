from __future__ import unicode_literals

from django.db import models

# Create your models here.
import accounts.models
from app import models as app_models


class Cart(models.Model):
    user_id = models.ForeignKey(accounts.models.Customers, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id.name


class CartLine(models.Model):
    product_id = models.ForeignKey(app_models.Product, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE);
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(blank=False);

    def __str__(self):
        return self.cart_id.id + " , " + self.product_id.product_name


def get_user_cart(customer):
    try:
        cart = Cart.objects.get(user_id=customer)
    except Cart.DoesNotExist:
        cart = Cart(user_id=customer)
        cart.save()
    return cart


def add_product_to_cartline(cart, product, quantity):
    try:
        cart_line = CartLine.objects.get(cart_id=cart, product_id=product)
        cart_line.quantity = cart_line.quantity + quantity;
        cart_line.save();
    except CartLine.DoesNotExist:
        cart_line = CartLine(cart_id=cart, product_id=product, quantity=quantity);
        cart_line.save();


def get_cart_line_items(cart):
    items = CartLine.objects.filter(cart_id=cart);
    return items

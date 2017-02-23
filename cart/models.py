from __future__ import unicode_literals

from django.db import models

# Create your models here.
import accounts.models
from app import models as app_models


class Cart(models.Model):
    user_id = models.ForeignKey(accounts.models.Customers, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


class CartLine(models.Model):
    product_id = models.ForeignKey(app_models.Product, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE);
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(blank=False);

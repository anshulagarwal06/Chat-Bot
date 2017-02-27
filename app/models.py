from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    create_at = models.DateTimeField(auto_now_add=True);

    def __str__(self):
        return self.category_name;


@python_2_unicode_compatible
class Product(models.Model):
    """docstring for product"""
    product_name = models.CharField(max_length=100);
    is_active = models.BooleanField(default=True);
    Category = models.ForeignKey(Category, on_delete=models.CASCADE);

    def __str__(self):
        return "product : " + self.product_name + " , active : " + str(
            self.is_active)

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Category(models.Model):
	category_name=models.CharField(max_length=50);
	create_at=models.DateTimeField();

class Product(models.Model):
	"""docstring for product"""
	product_name = models.CharField(max_length=100);
	price = models.DecimalField(max_digits=5 ,decimal_places = 2)
	is_active = models.BooleanField(default = True);
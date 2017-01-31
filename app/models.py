from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Category(models.Model):
	category_name=models.CharField(max_length=50);
	create_at=models.DateTimeField();

	def __str__(self):
		return self.category_name;



@python_2_unicode_compatible
class Product(models.Model):
	"""docstring for product"""
	product_name = models.CharField(max_length=100);
	price = models.DecimalField(max_digits=5 ,decimal_places = 2)
	is_active = models.BooleanField(default = True);
	Category =  models.ForeignKey(Category, on_delete=models.CASCADE);


	def __str__(self):
		return "product_name : " + self.product_name +", price : " + str(self.price) + " , is_active : " + str(self.is_active)


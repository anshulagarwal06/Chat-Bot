from __future__ import unicode_literals
from django.db import models
from address.models import Addresses


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=20)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True);

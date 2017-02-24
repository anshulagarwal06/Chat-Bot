from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Addresses(models.Model):
    latitude = models.DecimalField(decimal_places=6, max_digits=10)
    longitude = models.DecimalField(decimal_places=6, max_digits=10)
    title = models.CharField(max_length=20)
    address = models.CharField(max_length=200);
    create_at = models.DateTimeField(auto_now_add=True);

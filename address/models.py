from __future__ import unicode_literals

from django.db import models

from accounts.models import Customers


# Create your models here.

class Addresses(models.Model):
    latitude = models.DecimalField(decimal_places=6, max_digits=10)
    longitude = models.DecimalField(decimal_places=6, max_digits=10)
    title = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True);
    create_at = models.DateTimeField(auto_now_add=True);


class CustomerAddress(models.Model):
    user = models.ForeignKey(Customers, on_delete=models.CASCADE);
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE);
    create_at = models.DateTimeField(auto_now_add=True);
    default = models.BooleanField(default=False)

    def create_customer_address(self):
        customer_addresses = CustomerAddress.objects.filter(customers_id=self.user.pk, default=True)

        for customer_address in customer_addresses:
            customer_address.default = False
            customer_address.save()

        self.default = True;
        self.save();

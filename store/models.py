from __future__ import unicode_literals
from django.db import models
from address.models import Addresses
from geopy.distance import vincenty

min_circle_radius = 200;


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=20)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True);

    def __str__(self):
        return self.name


# class StoreAddress(models.Model):
#     store = models.OneToOneField(Store, on_delete=models.CASCADE)
#     address = models.ForeignKey(Addresses, on_delete=models.CASCADE);
#     create_at = models.DateTimeField(auto_now_add=True);
#
#     def __str__(self):
#         return  self.store.name


def get_stores(lat, longitude):
    # Need to modify, Very unoptimized solution for now.
    # work for very few store(doing only for POC)

    store_address = Store.objects.all();
    customer_loc = (lat, longitude);

    store_list = [];
    for store in store_address:
        print "Store : " + store.name

        s_lat = store.address.latitude
        s_long = store.address.longitude
        store_loc = (s_lat, s_long)
        distance = vincenty(store_loc, customer_loc).meters
        distance = abs(distance);
        print "Store : " + store.name + "distance : " + str(distance);
        if distance <= min_circle_radius:
            store_list.append(store)

    return store_list

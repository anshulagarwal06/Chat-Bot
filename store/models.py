from __future__ import unicode_literals
from django.db import models
from address.models import Addresses
from app.models import Product
from accounts.models import Customers

from geopy.distance import vincenty

min_circle_radius = 200;


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=20)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True);

    def __str__(self):
        return self.name


class StoreCustomer(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers);

    def __str__(self):
        return self.customer.name


class StoreProducts(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE);
    create_at = models.DateTimeField(auto_now_add=True);
    price = models.DecimalField(decimal_places=2, blank=False, null=False, max_digits=7)
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.store.name + " , " + self.product.product_name


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


def get_customers_store(customer):
    # get store that is connect to this customer
    return StoreCustomer.objects.get(customer_id=customer.pk).store


def get_store_category(store):
    products = StoreProducts.objects.filter(store_id=store.pk, active=True);
    distinct_cat = products.values_list('product__Category').distinct("product__Category_id");
    print "distinct cat " + distinct_cat
    return distinct_cat;


def connect_store_to_customer(store_id, customer):
    store = Store.objects.get(id=store_id)

    try:
        store_customer = StoreCustomer.objects.get(customer_id=customer.pk);
        store_customer.store = store;
        store_customer.save()
    except StoreCustomer.DoesNotExist:
        store_customer = StoreCustomer(store=store, customer=customer)
        store_customer.save()

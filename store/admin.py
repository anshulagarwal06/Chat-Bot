from django.contrib import admin
from .models import Store, StoreCustomer, StoreProducts

admin.site.register(Store)
admin.site.register(StoreCustomer)
admin.site.register(StoreProducts)

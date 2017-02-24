from django.contrib import admin

# Register your models here.
from .models import Addresses, CustomerAddress

admin.site.register(Addresses)
admin.site.register(CustomerAddress)

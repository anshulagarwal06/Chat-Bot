from accounts.models import Customers
from rest_framework import serializers


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('id', 'name', 'email', 'phone_number', 'profile_picture', 'fb_id');

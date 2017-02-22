from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Customers(models.Model):
    name = models.CharField(max_length=50);
    email = models.CharField(max_length=50, default='', blank=True);
    phone_number = models.CharField(max_length=50, default='', blank=True);
    create_at = models.DateTimeField(auto_now_add=True);
    profile_picture = models.CharField(max_length=200, default='', blank=True);
    fb_id = models.CharField(max_length=50, unique=True);

    def __str__(self):
        return 'name : ' + self.name + ' email : ' + self.email + 'phone_number : ' + self.phone_number + \
               'profile_picture : ' + self.profile_picture + 'fb_id : ' + self.fb_id

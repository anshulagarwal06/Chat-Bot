from __future__ import unicode_literals

import requests
from django.db import models
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
        return 'name : ' + self.name


def fetch_customers_details(sender_id):
    try:
        customer = Customers.objects.get(fb_id=sender_id)
    except Customers.DoesNotExist:
        customer = None

    if customer is None:
        url = "https://graph.facebook.com/v2.8/" + sender_id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAAWS4fk3smoBAIyUdqQbKZCjICHwr2ZAkVhM8oDOyppnZBoJLNeQ5IjeAUrlf5X3jYV0rxvZCs0eZABSH79eCpUBHeosZBPiB3QUYrYAP7kmgwfCS6DfTQZASj05RgmFRcdjSfXaVrpnZChcvQEUH1ZBY9GFCZAJb1g87ie4uBQcNQ1QZDZD"
        response = requests.get(url);
        json_data = response.json();
        print " Profile json_data" + str(json_data);
        if 'first_name' in json_data:
            name = json_data['first_name'] + " " + json_data["last_name"]
            profile_picture = json_data['profile_pic']
            fb_id = sender_id;

            customer = Customers(name=name, profile_picture=profile_picture, fb_id=fb_id)
            customer.save();
            return customer;
        else:
            print " Empty data from fb"
            return None

    else:
        return customer;

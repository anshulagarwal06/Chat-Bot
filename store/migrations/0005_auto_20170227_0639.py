# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-27 06:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('store', '0004_storecustomer_storeproducts'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='storeproducts',
            unique_together=set([('store', 'product')]),
        ),
    ]
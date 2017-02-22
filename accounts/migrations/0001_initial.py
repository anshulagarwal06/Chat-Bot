# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-22 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(blank=True, default='', max_length=50)),
                ('phone_number', models.CharField(blank=True, default='', max_length=50)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('profile_picture', models.CharField(blank=True, default='', max_length=200)),
                ('fb_id', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-26 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_auto_20170224_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresses',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
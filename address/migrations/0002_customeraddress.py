# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-24 09:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('default', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.Addresses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Customers')),
            ],
        ),
    ]

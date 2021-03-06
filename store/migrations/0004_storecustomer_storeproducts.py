# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-26 12:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('app', '0001_initial'),
        ('store', '0003_auto_20170226_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Customers')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
            ],
        ),
        migrations.CreateModel(
            name='StoreProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
            ],
        ),
    ]

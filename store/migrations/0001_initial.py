# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-24 07:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.Addresses')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-03 14:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0011_auto_20160802_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gig',
            name='admin',
        ),
    ]

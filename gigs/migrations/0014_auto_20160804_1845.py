# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-04 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0013_role_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='approved',
            field=models.NullBooleanField(),
        ),
    ]

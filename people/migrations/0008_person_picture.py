# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-01 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_auto_20160731_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='picture',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]

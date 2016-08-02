# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-02 09:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gigs', '0007_auto_20160731_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gig',
            name='owner',
        ),
        migrations.AddField(
            model_name='gig',
            name='admin',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]

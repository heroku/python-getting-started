# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-06 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='created_at',
        ),
        migrations.AddField(
            model_name='role',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='role',
            name='end_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='start_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
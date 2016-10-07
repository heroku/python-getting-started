# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-07 18:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0006_auto_20161006_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('invitee', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='inviteds', to=settings.AUTH_USER_MODEL)),
                ('inviter', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='invites', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='teams.Team')),
            ],
        ),
    ]

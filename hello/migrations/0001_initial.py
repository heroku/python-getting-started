# Generated by Django 5.2 on 2025-04-06 14:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Greeting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "when",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 5.0.2 on 2024-08-03 10:32

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dataCollector", "0006_hourlyaverage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hourlyaverage",
            name="hour",
            field=django_jalali.db.models.jDateTimeField(unique=True),
        ),
    ]

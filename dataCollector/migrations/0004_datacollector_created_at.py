# Generated by Django 5.0.2 on 2024-06-02 13:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataCollector', '0003_device_sn'),
    ]

    operations = [
        migrations.AddField(
            model_name='datacollector',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

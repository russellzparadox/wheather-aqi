# Generated by Django 5.0.2 on 2024-03-04 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataCollector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Lat', models.FloatField()),
                ('Lng', models.FloatField()),
                ('Humidity', models.FloatField()),
                ('Temperature', models.FloatField()),
                ('CO', models.FloatField()),
                ('H2', models.FloatField()),
                ('LPG', models.FloatField()),
                ('CH4', models.FloatField()),
                ('NOx', models.FloatField()),
                ('CL2', models.FloatField()),
                ('Alchohol', models.FloatField()),
                ('CO2', models.FloatField()),
                ('Toluen', models.FloatField()),
                ('NH4', models.FloatField()),
                ('Aceton', models.FloatField()),
                ('PM1_0', models.FloatField()),
                ('PM2_5', models.FloatField()),
                ('PM10', models.FloatField()),
            ],
        ),
    ]

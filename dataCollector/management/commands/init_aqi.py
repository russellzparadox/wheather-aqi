from django.core.management.base import BaseCommand
from django.db.models import Avg, Min
from dataCollector.models import DataCollector, HourlyAverage
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Calculates and logs the hourly average of data from the beginning of the data till now"

    def handle(self, *args, **kwargs):
        average_data_query = HourlyAverage.objects.all()
        for i in average_data_query:
            if i.aqi is None:
                i.aqi = i.calculate_aqi()
                i.save()


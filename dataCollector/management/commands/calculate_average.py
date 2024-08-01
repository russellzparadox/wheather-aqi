from django.core.management.base import BaseCommand
from dataCollector.models import DataCollector  # Replace with your model
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Calculates and logs the average of data every hour"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        if now.minute == 0:
            # Perform the average calculation
            data = DataCollector.objects.filter(
                created_at__gte=now - timedelta(hours=1), created_at__lte=now
            )
            print("fuck?")
            # average = data.aggregate(Avg('field_name'))['field_name__avg']  # Replace 'field_name' with your field
            # self.stdout.write(self.style.SUCCESS(f'Average calculated: {average}'))
        print("no fuck")
